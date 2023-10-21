import os
import sys

import cv2
import paddle
import paddleocr
from paddleocr.ppocr.utils.network import download_with_progressbar
from paddleocr.ppocr.utils.utility import check_and_read, get_image_file_list
from paddleocr.ppstructure.predict_system import save_structure_res
from paddleocr.ppstructure.utility import init_args

paddleocr_path = os.environ.get('PADDLEOCR_PATH')
if paddleocr_path:
    sys.path.insert(0, paddleocr_path)


def str2bool(v):
    return v.lower() in ("true", "yes", "t", "y", "1")


def is_link(s):
    return s is not None and s.startswith('http')


def version():
    print(f"Python Version: {sys.version}")
    print(f"Paddle Version: {paddle.__version__}")
    print(f"PaddleOCR Version: {paddleocr.__version__}")


def ocrOutputText(source, language):
    # 检测+方向分类器+识别全流程
    ocr = paddleocr.PaddleOCR(use_angle_cls=True,
                              lang=language)  # need to run only once to download and load model into memory

    result = ocr.ocr(source, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            coordinates, content_info = line  # 解包line
            text, confidence = content_info  # 解包content_info
            print(text)


def parse_args(mMain=True):
    import argparse
    parser = init_args()
    parser.add_help = mMain
    parser.add_argument("--lang", type=str, default='ch')
    parser.add_argument("--det", type=str2bool, default=True)
    parser.add_argument("--rec", type=str2bool, default=True)
    parser.add_argument("--type", type=str, default='ocr')
    parser.add_argument(
        "--ocr_version",
        type=str,
        choices=paddleocr.paddleocr.SUPPORT_OCR_MODEL_VERSION,
        default='PP-OCRv4',
        help='OCR Model version, the current model support list is as follows: '
             '1. PP-OCRv4/v3 Support Chinese and English detection and recognition model, and direction classifier model'
             '2. PP-OCRv2 Support Chinese detection and recognition model. '
             '3. PP-OCR support Chinese detection, recognition and direction classifier and multilingual recognition model.'
    )
    parser.add_argument(
        "--structure_version",
        type=str,
        choices=paddleocr.paddleocr.SUPPORT_STRUCTURE_MODEL_VERSION,
        default='PP-StructureV2',
        help='Model version, the current model support list is as follows:'
             ' 1. PP-Structure Support en table structure model.'
             ' 2. PP-StructureV2 Support ch and en table structure model.')

    # 添加参数
    parser.add_argument('-ot', '--output_type', type=str, help='toutput text default is text')
    parser.add_argument('-v', '--version', action='store_true', help='version')
    parser.add_argument('-src', '--source', type=str, help='source file path')

    for action in parser._actions:
        if action.dest in [
            'rec_char_dict_path', 'table_char_dict_path', 'layout_dict_path'
        ]:
            action.default = None
    if mMain:
        return parser.parse_args()
    else:
        inference_args_dict = {}
        for action in parser._actions:
            inference_args_dict[action.dest] = action.default
        return argparse.Namespace(**inference_args_dict)


def main():
    # for cmd
    args = parse_args(mMain=True)

    # 根据参数执行相应的操作
    if args.version:
        return version()

    if args.output_type:
        return ocrOutputText(args.source, args.lang);

    image_dir = args.image_dir
    if is_link(image_dir):
        download_with_progressbar(image_dir, 'tmp.jpg')
        image_file_list = ['tmp.jpg']
    else:
        image_file_list = get_image_file_list(args.image_dir)
    if len(image_file_list) == 0:
        paddleocr.paddleocr.logger.error('no images find in {}'.format(args.image_dir))
        return
    if args.type == 'ocr':
        engine = paddleocr.PaddleOCR(**(args.__dict__))
    elif args.type == 'structure':
        engine = paddleocr.PPStructure(**(args.__dict__))
    else:
        raise NotImplementedError

    for img_path in image_file_list:
        img_name = os.path.basename(img_path).split('.')[0]
        paddleocr.paddleocr.logger.info('{}{}{}'.format('*' * 10, img_path, '*' * 10))
        if args.type == 'ocr':
            ocrType(args, engine, img_path, args.output, img_name)
        elif args.type == 'structure':
            img, flag_gif, flag_pdf = check_and_read(img_path)
            if not flag_gif and not flag_pdf:
                img = cv2.imread(img_path)

            if args.recovery and args.use_pdf2docx_api and flag_pdf:
                from pdf2docx.converter import Converter
                docx_file = os.path.join(args.output,
                                         '{}.docx'.format(img_name))
                cv = Converter(img_path)
                cv.convert(docx_file)
                cv.close()
                paddleocr.paddleocr.logger.info('docx save to {}'.format(docx_file))
                continue

            if not flag_pdf:
                if img is None:
                    paddleocr.paddleocr.logger.error("error in loading image:{}".format(img_path))
                    continue
                img_paths = [[img_path, img]]
            else:
                img_paths = []
                for index, pdf_img in enumerate(img):
                    os.makedirs(
                        os.path.join(args.output, img_name), exist_ok=True)
                    pdf_img_path = os.path.join(
                        args.output, img_name,
                        img_name + '_' + str(index) + '.jpg')
                    cv2.imwrite(pdf_img_path, pdf_img)
                    img_paths.append([pdf_img_path, pdf_img])

            all_res = []
            for index, (new_img_path, img) in enumerate(img_paths):
                paddleocr.paddleocr.logger.info('processing {}/{} page:'.format(index + 1,
                                                                                len(img_paths)))
                new_img_name = os.path.basename(new_img_path).split('.')[0]
                result = engine(img, img_idx=index)
                save_structure_res(result, args.output, img_name, index)

                if args.recovery and result != []:
                    from copy import deepcopy
                    from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes
                    h, w, _ = img.shape
                    result_cp = deepcopy(result)
                    result_sorted = sorted_layout_boxes(result_cp, w)
                    all_res += result_sorted

            if args.recovery and all_res != []:
                try:
                    from paddleocr.ppstructure.recovery.recovery_to_doc import convert_info_docx
                    convert_info_docx(img, all_res, args.output, img_name)
                except Exception as ex:
                    paddleocr.paddleocr.logger.error(
                        "error in layout recovery image:{}, err msg: {}".format(
                            img_name, ex))
                    continue

            for item in all_res:
                item.pop('img')
                item.pop('res')
                paddleocr.paddleocr.logger.info(item)
            paddleocr.paddleocr.logger.info('result save to {}'.format(args.output))


def ocrType(args, engine, img_path, output, img_name):
    result = engine.ocr(img_path,
                        det=args.det,
                        rec=args.rec,
                        cls=args.use_angle_cls,
                        bin=args.binarize,
                        inv=args.invert,
                        alpha_color=args.alphacolor)

    if result is not None:
        full_text = ""  # 初始化一个空的字符串变量
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                paddleocr.paddleocr.logger.info(line)
                coordinates, content_info = line  # 解包line
                text, confidence = content_info  # 解包content_info
                full_text += text + "\n"  # 将每一行的文本结果追加到full_text
        if output:
            if not os.path.exists(output):
                os.mkdir(output)
            output_file = os.path.join(args.output, '{}.txt'.format(img_name))
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)  # 将full_text写入output_file

