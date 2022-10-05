import os, sys, argparse


def set_path():
    """
    * 경로 잡기
    """

    # 경로명 설정
    AppPath = os.path.dirname(os.path.abspath(os.getcwd()))
    SRC_DIR_NAME_Common = 'Common'
    SRC_DIR_NAME_DATA = 'DATA'
    SRC_DIR_NAME_DeepLearning = 'DeepLearning'
    SRC_DIR_NAME_Lib = 'Lib'
    SRC_DIR_NAME_LOG = 'LOG'
    SRC_DIR_NAME_Main = 'Main'
    SRC_DIR_NAME_RES = 'RES'

    Common = os.path.join(AppPath, SRC_DIR_NAME_Common)
    DATA = os.path.join(AppPath, SRC_DIR_NAME_DATA)
    DeepLearning = os.path.join(AppPath, SRC_DIR_NAME_DeepLearning)
    Lib = os.path.join(AppPath, SRC_DIR_NAME_Lib)
    LOG = os.path.join(AppPath, SRC_DIR_NAME_LOG)
    Main = os.path.join(AppPath, SRC_DIR_NAME_Main)
    RES = os.path.join(AppPath, SRC_DIR_NAME_RES)

    # 경로 추가
    AppPathList = [AppPath, Common, DATA, DeepLearning, Lib, LOG, Main, RES]
    for p in AppPathList:
        sys.path.append(p)


def arguments():
    """
    * parser 이용하여 프로그램 실행 인자 받기
    :return: args
    """

    from Common import ConstVar

    # parser 에서 사용될 선택지 목록. 실행 모드
    runningModeList = [
        ConstVar.RUNNING_MODE_DEPLOY,
        ConstVar.RUNNING_MODE_DEV
    ]

    # parser 생성
    parser = argparse.ArgumentParser(prog="MovementsDTXSL",
                                     description="* Data Extraction Automation.")

    # parser 인자 목록 생성
    # 실행 모드 선택
    parser.add_argument("--running_mode",
                        type=str,
                        help='running mode selection ({0} / {1})'.format(
                            ConstVar.RUNNING_MODE_DEPLOY,
                            ConstVar.RUNNING_MODE_DEV
                        ),
                        choices=runningModeList,
                        default=ConstVar.RUNNING_MODE_DEPLOY,
                        dest="runningMode")

    # CSV 파일 경로 또는 해당 디렉터리 설정
    parser.add_argument("--csv_path_or_dir",
                        type=str,
                        help='write CSV file path for single file, or CSV file directory for multiple files',
                        default=ConstVar.CSV_DIR,
                        dest="csv_path_or_dir")

    # 결과물 저장될 디렉터리 설정
    parser.add_argument("--output_dir",
                        type=str,
                        help='write output directory',
                        default=ConstVar.OUTPUT_DIR,
                        dest='output_dir')

    # parsing 한거 가져오기
    args = parser.parse_args()

    return args


def run_program(args):
    """
    * 프로그램 실행
    :param args: 프로그램 실행 인자
    :return: None
    """



def main():

    # 경로 잡기
    set_path()

    # 인자 받기
    args = arguments()

    # 프로그램 실행
    run_program(args=args)


if __name__ == '__main__':
    main()