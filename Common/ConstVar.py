import os, datetime

# 파일 경로
PROJECT_ROOT_DIRECTORY = os.path.dirname(os.getcwd())
DATA_DIR_TRAIN = '{0}/RES/SIGNS dataset/train_signs/'.format(PROJECT_ROOT_DIRECTORY)
DATA_DIR_TEST = '{0}/RES/SIGNS dataset/test_signs/'.format(PROJECT_ROOT_DIRECTORY)
OUTPUT_DIR_CHECKPOINT = '{0}/DATA/checkpoint/'.format(PROJECT_ROOT_DIRECTORY)
CHECKPOINT_FILE_NAME = 'epoch{:05d}.ckpt'
CHECKPOINT_BEST_FILE_NAME = 'best_model.ckpt'

# 학습 / 테스트 모드
MODE_TRAIN = 'train'
MODE_TEST = 'test'

# 디바이스 종류
DEVICE_CUDA = 'cuda'
DEVICE_CPU = 'cpu'

# 하이퍼 파라미터
RESIZE_SIZE = 32
LEARNING_RATE = 0.001
BATCH_SIZE = 4
SHUFFLE = True
NUM_EPOCH = 2

# state 저장시 딕셔너리 키 값
KEY_STATE_MODEL = 'model'
KEY_STATE_OPTIMIZER = 'optimizer'
KEY_STATE_EPOCH = 'epoch'

#
INITIAL_START_EPOCH_NUM = 1
