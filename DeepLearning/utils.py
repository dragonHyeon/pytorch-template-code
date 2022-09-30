import torch

from Common import ConstVar
from Lib import UtilLib


def load_checkpoint(filepath):
    """
    * 체크포인트 불러오기
    :param filepath: 불러올 체크포인트 파일 경로
    :return: state 모음 (model.state_dict(), optimizer.state_dict(), epoch)
    """

    # state 불러오기
    state = torch.load(f=filepath)

    # state 정보 리턴
    return state


def save_checkpoint(filepath, model, optimizer=None, epoch=None, is_best=False):
    """
    * 체크포인트 저장
    :param filepath: 저장될 체크포인트 파일 경로
    :param model: 저장될 모델
    :param optimizer: 저장될 optimizer
    :param epoch: 저장될 현재 학습 epoch 횟수
    :param is_best: 현재 저장하려는 모델이 가장 좋은 성능의 모델인지 여부
    :return: 체크포인트 파일 생성됨
    """

    # state 정보 담기
    state = {
        ConstVar.KEY_STATE_MODEL: model.state_dict(),
        ConstVar.KEY_STATE_OPTIMIZER: optimizer.state_dict(),
        ConstVar.KEY_STATE_EPOCH: epoch
    }

    # state 저장
    torch.save(obj=state,
               f=filepath)

    # 현재 저장하려는 모델이 가장 좋은 성능의 모델인 경우 best model 로 저장
    if is_best:
        torch.save(obj=state,
                   f=UtilLib.getNewPath(path=UtilLib.getParentDirPath(filePath=filepath),
                                        add=ConstVar.CHECKPOINT_BEST_FILE_NAME))
