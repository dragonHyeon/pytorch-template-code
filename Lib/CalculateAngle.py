"""
* 각도 계산 모듈
"""
import traceback
import math
from decimal import Decimal
# import geopy.distance as geopyDistance

#------------------------------------------
# * 고정변수
# 1) 에러 값 숫자
Error_Value = math.nan
# 2) 에러 값 문자
Error_String = "ERROR"
# 3) DTX 회전각 변수
## azimuth
Degree_Azimuth = "AZIMUTH"
## yaw
Degree_Yaw = "YAW"
## pitch
Degree_Pitch = "PITCH"
## roll
Degree_Roll = "ROLL"
# 4) Blender, Unity 회전각 변수
RotationX = "RX"
RotationY = "RY"
RotationZ = "RZ"
#------------------------------------------

# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
def _convertDegreeToRadian(degreeValue):
    """
    * 각도 단위계 변환 (degree-> Radian)
    - Created Date : 2021.10.12
    - Created by JSLee
    - JAVA version method : deg2rad()

    :param degreeValue: 변환 할 degree 값
    :return: 변환 된  Radian 값
    """
    # 최종 결과 변수
    resultRadian = Error_Value

    try:
        ## 1) java version (mingyu kim)
        # deg * Math.PI / 180.0

        ## 2) convert python version
        # step1Value = Decimal(degreeValue) * Decimal(math.pi)
        # step2Value = Decimal(step1Value) / Decimal(180.0)
        # resultRadian = step2Value

        ## 3) python math library
        resultRadian = math.radians(degreeValue)


    except Exception as err:
        print("[method : _convertDegreeToRadian] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultRadian

def _convertRadianToDegree(radianValue):
    """
    * 각도 단위계 변환 (radian -> degree)
    - Created Date : 2021.10.12
    - Created by JSLee
    - JAVA version method : rad2deg()
    :param radianValue: 변환 할 radian 값
    :return: 변환 된 degree 값
    """
    # 최종 결과 변수
    resultDegree = Error_Value

    try:
        ## 1) java version (mingyu mim)
        # rad * 180.0 / Math.PI

        ## 2) convert python version
        # step1Value = Decimal(radianValue) * Decimal(180.0)
        # step2Value = Decimal(step1Value) / Decimal(math.pi)
        # resultDegree = step2Value

        ## 3) python math library
        resultDegree = math.degrees(radianValue)

    except Exception as err:
        print("[method : _convertRadianToDegree] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDegree

def _convert3AxisRotationDegree(degreeValue):
    """
    * 북쪽 축 방향을 기준으로 시계 방향의 각도로 반환
    - Created Date : 2021.10.21
    - Created by JSLee
    - 두점 기준으로 회전각(azimuth, pitch, roll)을 구하여 DB에 저장할떄 사용
    - xy 평면 : y축 0도 기준
    - yz 평면 : z축 0도 기준
    - xz 평면 : z축 0도 기준
    :param degreeValue: 변환할 degree 값(동쪽 기준 각도, degreeValue <= 360 임)
    :return: 변환 된 degree값
    """
    # 최종 결과 변수
    resultDegree = Error_Value

    try:
        resultDegree = (360 - degreeValue + 90) % 360
    except Exception as err:
        print("[method : _convert3AxisRotationDegree] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDegree

def _convert3AxisRotationDegreeForBlender(degreeValue):
    """
    * blender에서 사용할 Rotation 각도로 변환
    - Created Date : 2021.10.22
    - Created by JSLee
    - xy 평면 : y축 0도 기준
    - yz 평면 : z축 0도 기준
    - xz 평면 : z축 0도 기준
    :param degreeValue: 변환할 degree 값(각축의 북쪽 방향 기준 각도)
    :return: 변환 된 degree값
    """
    # DTX의 3축 회전각 A, Blender의 3축 회전각 B 라 할때
    # A + B = 360 degree
    # B = 360 - A

    # 최종 결과 변수
    resultDegree = Error_Value

    try:
        resultDegree = Decimal(360) - Decimal(degreeValue)
    except Exception as err:
        print("[method : _convert3AxisRotationDegreeForBlender] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDegree

def _convert3AxisRotationDegreeForUnity(degreeValue):
    """
    * Unity에서 사용할 Rotation 각도로 변환
    - Created Date : 2021.10.22
    - Created by JSLee
    - xy 평면 : y축 0도 기준
    - yz 평면 : z축 0도 기준
    - xz 평면 : z축 0도 기준
    :param degreeValue: 변환할 degree 값(각축의 북쪽 방향 기준 각도)
    :return: 변환 된 degree값
    """
    # DTX의 3축 회전각 A, Unity의 3축 회전각 C 라고 할때
    # A = B 임

    # 최종 결과 변수
    resultDegree=Error_Value

    try:
        resultDegree = degreeValue
    except Exception as err:
        print("[method : _convert3AxisRotationDegreeForUnity] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDegree

def _getAzimuthWGS84(startLatitude, startLongitude, endLatitude, endLongitude):
    """
    * 방위각(azimuth) 값 반환 (WGS84 타원체 EPSG:4326좌표계 사용시) - 파리미터 단위 degree
      웹에서 사용
    - Create Date : 2021.10.14
    - Create by JSLee
    - JAVA version method : azimuthWGS84()    
    :param startLatitude: 시작점 위도(EPSG:4326좌표계, degree, 도)
    :param startLongitude: 시작점 경도(EPSG:4326좌표계, degree, 도)
    :param endLatitude: 끝점 위도(EPSG:4326좌표계, degree, 도)
    :param endLongitude: 끝점 경도(EPSG:4326좌표계, degree, 도)
    :return: 방위각(degree, 도)
    """

    # 최종 결과 변수
    resultDegree = Error_Value

    try:
        # Step1) 좌표계 변환 - 공간분석시 degree단위계(EPSG:4326좌표계)를 사용하지 않고 meter 단위계를 사용해야함
        # 입력된 시작점, 끝점 좌표(경위도 좌표계,WGS84, EPSG4326 , unit : degree)를
        # radian(unit : meter)으로 변환한다
        radian_startLat = _convertDegreeToRadian(degreeValue=startLatitude)  # 위도 좌표 변환
        radian_startLon = _convertDegreeToRadian(degreeValue=startLongitude)  # 경도 좌표 변환
        radian_endLat = _convertDegreeToRadian(degreeValue=endLatitude)  # 위도 좌표 변환
        radian_endLon = _convertDegreeToRadian(degreeValue=endLongitude)  # 경도 좌표 변환

        # Step2) 좌표간의 차이값 계산
        dx = radian_endLat - radian_startLat
        dy = radian_endLon - radian_startLon

        # Step3) 방위각 계산
        # 계산된 값이 radian 으로 나오는 것을 degree로 변환하여 결과값 반환
        y = math.sin(dy) * math.cos(radian_endLat)
        x = math.cos(radian_startLat) * math.sin(radian_endLat) - math.sin(radian_startLat) * math.cos(radian_endLat) * math.cos(dy)

        radian_bearing = math.atan2(y, x)
        degree_bearing = (_convertRadianToDegree(radianValue=radian_bearing) + 360) % 360
        resultDegree = degree_bearing
    except Exception as err:
        print("[method : _getAzimuthWGS84] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDegree

def _getAzimuthGRS80(startLatitude, startLongitude, endLatitude, endLongitude):
    """
    * 방위각(azimuth) 값 반환 (GRS80 타원체, EPSG:5286 사용시) - 파리미터 단위 meter
      AR 과 같은 2차원 평면에서 사용
    - Create Date : 2021.10.14
    - Create by JSLee
    - JAVA version method : azimuthGRS80()
    :param startLatitude: 시작점 위도(EPSG:5286좌표계, meter)
    :param startLongitude: 시작점 경도(EPSG:5286좌표계, meter)
    :param endLatitude: 끝점 위도(EPSG:5286좌표계, meter)
    :param endLongitude: 끝점 경도(EPSG:5286좌표계, meter)
    :return: 방위각(degree, 도)
    """

    # 최종 결과 변수
    resultDegree = Error_Value

    try:
        # Step1) 방위각 계산
        y = startLongitude - endLongitude
        x = startLatitude - endLatitude

        radian_bearing = math.atan2(y, x)
        degree_bearing = _convertRadianToDegree(radianValue=radian_bearing) + 180

        if degree_bearing < 0.0:
            resultDegree = degree_bearing + 360
        else:
            resultDegree = degree_bearing
    except Exception as err:
        print("[method : _getAzimuthGRS80] Exception Error : {}".format(err))
        #print("parameter : ({}, {}) || ({}, {})".format(startLatitude,startLongitude,endLatitude,endLongitude))
        print(traceback.format_exc())

    return resultDegree

def _getDistanceWGS84(startLatitude, startLongitude, endLatitude, endLongitude):
    """
    * 두점 사이의 거리 구하기(웹 구면에서 사용)
    - Created Date : 2021.10.24
    - Created by JSLee
    - Haversine distance 방법을 사용(geo 라이브러리 사용 안함)
    - reference : http://daplus.net/python-%EC%9C%84%EB%8F%84-%EA%B2%BD%EB%8F%84%EB%A5%BC-%EA%B8%B0%EC%A4%80%EC%9C%BC%EB%A1%9C-%EB%91%90-%EC%A0%90-%EC%82%AC%EC%9D%B4%EC%9D%98-%EA%B1%B0%EB%A6%AC-%EC%96%BB%EA%B8%B0/
    :param startLatitude: 시작점 위도(EPSG:4326좌표계, degree, 도) x
    :param startLongitude: 시작점 경도(EPSG:4326좌표계, degree, 도) y
    :param endLatitude: 끝점 위도(EPSG:4326좌표계, degree, 도) x
    :param endLongitude: 끝점 경도(EPSG:4326좌표계, degree, 도) y
    :return: 계산된 거리값 (단위 : meter)
    """
    # 최종 결과 변수
    resultDistance = Error_Value

    try:
        # Step1) 입력한 경위도 좌표(degree)를 radian 으로 변환
        radian_startLat = _convertDegreeToRadian(degreeValue=startLatitude)  # 위도 좌표 변환
        radian_startLon = _convertDegreeToRadian(degreeValue=startLongitude)  # 경도 좌표 변환
        radian_endLat = _convertDegreeToRadian(degreeValue=endLatitude)  # 위도 좌표 변환
        radian_endLon = _convertDegreeToRadian(degreeValue=endLongitude)  # 경도 좌표 변환
        # Step2) 경위도 값의 차 구하기
        radian_dy = radian_endLon - radian_startLon
        radian_dx = radian_endLat - radian_startLat

        # Step3) 거리 구하기 3가지 타입
        """
        ## 1) java version 코드 구현 
        theta = endLongitude - startLongitude
        radian_theta = _convertDegreeToRadian(degreeValue=theta)
        dist = math.sin(radian_startLat) * math.sin(radian_endLat) + math.cos(radian_startLat) * math.cos(radian_endLat) * math.cos(radian_theta)
        dist = math.acos(dist)
        dist = _convertRadianToDegree(radianValue=dist)
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344 * 1000
        resultDistance = dist    
        #"""

        """
        ## 2) geopy distance 계산
        # java version 과 50cm 정도 차이남
        startPoint = (startLatitude, startLongitude)
        endPoint = (endLatitude, endLongitude)
        resultGeopyDistatnce = geopyDistance.distance(startPoint, endPoint).m   # .m : km -> m 단위로 변환함
        resultDistance = resultGeopyDistatnce
        print(resultDistance)
        #"""

        ## method 3) 라이브러리 의존성 없이 계산
        # java version과 1cm 정도 차이남
        radius = 6371.0088  # 지구 평균 반지름 (단위 : km)
        a = (math.sin(radian_dx / 2) * math.sin(radian_dx / 2) + math.cos(radian_startLat) * math.cos(radian_endLat) * math.sin(radian_dy / 2) * math.sin(radian_dy /2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c * 1000   # km -> m 단위로 변환
        resultDistance = d
    except Exception as err:
        print("[method : _getDistanceWGS84] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDistance

def _getDistanceGRS80(startLatitude, startLongitude, endLatitude, endLongitude):
    """
    * 두점 사이의 거리 구하기(AR, 2차원 평면 에서 사용)
    - Created Date : 2021.10.24
    - Created by JSLee
    :param startLatitude: 시작점 위도(EPSG:4326좌표계, degree, 도)
    :param startLongitude: 시작점 경도(EPSG:4326좌표계, degree, 도)
    :param endLatitude: 끝점 위도(EPSG:4326좌표계, degree, 도)
    :param endLongitude: 끝점 경도(EPSG:4326좌표계, degree, 도)
    :return: 계산된 거리값 (단위 : meter)
    """
    # 최종 결과 변수
    resultDistance = Error_Value
    try:
        resultDistance = math.sqrt(math.pow(startLongitude - endLongitude, 2) + math.pow(startLatitude - endLatitude, 2))

    except Exception as err:
        print("[method : _getDistanceGRS80] Exception Error : {}".format(err))
        print(traceback.format_exc())

    return resultDistance



# ==============================================================================================================================
# ==============================================================================================================================
# ==============================================================================================================================
def getAllDegreeWGS84(startPoint, endPoint):
    """
    * 3축 회전각도 구하기(웹 구면에서 사용)
    - Created Date : 2021.10.21
    - Created by JSLee
    - dict key : AZIMUTH | PITCH | ROLL
    :param startPoint: 시작점(위도 y, 경도 x, 심도 z) tuple, WGS84 좌표
    :param endPoint: 종점(위도 y, 경도 x, 심도 z) tuple, WGS84 좌표
    :return: 3축 회전각 azimuth, pitch, roll 값이 들어있는 dict, WGS84 좌표
    """
    # 최종 결과값 저장
    resultAllDegreeDict = dict()

    # z축 고정하고 x-y 평면에 투영 => azimuth,yaw
    result1 = _getAzimuthWGS84(startPoint[0], startPoint[1], endPoint[0], endPoint[1])
    # 진북 방향으로 각도 변경
    azimuth = _convert3AxisRotationDegree(result1)

    # x축 고정하고 y-z 평면에 투영 => pitch
    result2 = _getAzimuthWGS84(startPoint[1], startPoint[2], endPoint[1], endPoint[2])
    # 진북 방향으로 각도 변경
    pitch = _convert3AxisRotationDegree(result2)

    # y축 고정하고 x-z 평면에 투영 => roll
    result3 = _getAzimuthWGS84(startPoint[0], startPoint[2], endPoint[0], endPoint[2])
    # 진북 방향으로 각도 변경
    roll = _convert3AxisRotationDegree(result3)

    # 최종 리턴 형태로 구성
    resultAllDegreeDict[Degree_Azimuth] = azimuth
    resultAllDegreeDict[Degree_Pitch] = pitch
    resultAllDegreeDict[Degree_Roll] = roll


    return resultAllDegreeDict


def getAllDegreeGRS80(startPoint, endPoint):
    """
    * 3축 회전각도 구하기(AR, 2차원 평면 에서 사용)
    - Created Date : 2021.10.21
    - Created by JSLee
    - dict key : AZIMUTH | PITCH | ROLL
    :param startPoint: 시작점(위거 Y_TM, 경거 X_TM, 심도 Z) tuple, GRS80 좌표
    :param endPoint: 종점(위거 Y_TM, 경거 X_TM, 심도 Z) tuple, GRS80 좌표
    :return: 3축 회전각 azimuth, pitch, roll 값이 들어있는 dict, GRS80 좌표
    """
    # 최종 결과값 저장
    resultAllDegreeDict = dict()

    # --------------------------------------------------------------------------------------
    # z축 고정하고 x-y 평면에 투영 => azimuth,yaw
    start_px = startPoint[0]
    start_py = startPoint[1]
    end_px = endPoint[0]
    end_py = endPoint[1]

    dy = end_py - start_py
    dx = end_px - start_px

    radianValue_azimuth = math.atan2(dy, dx)
    degreeValue_azimuth = _convertRadianToDegree(radianValue=radianValue_azimuth)


    if degreeValue_azimuth < 0:
        # atan2의 값의 범위가 -pi~pi 까지 이기 때문에 음수 값이 나옴
        # 이를 해결하기 위하여 음수 값이 나올경우에 한하여
        # degree 단위 일때 +360, radian 단위 일때 +2pi 를 하여
        # 음수값을 양수값으로 변환한다(-pi~pi 의 범위가 0~2pi 범위로 변경하는 것임)
        # 반시계 방향의 회전각임
        degreeValue_azimuth += 360
        #degreeValue_azimuth = degreeValue_azimuth % 360

    # 진북 방향으로 각도 변경
    degreeValue_azimuth = _convert3AxisRotationDegree(degreeValue=degreeValue_azimuth)

    # --------------------------------------------------------------------------------------
    # x축 고정하고 y-z 평면에 투영 => pitch
    start_px = startPoint[1]
    start_py = startPoint[2]
    end_px = endPoint[1]
    end_py = endPoint[2]

    dy = end_py - start_py
    dx = end_px - start_px

    radianValue_pitch = math.atan2(dy, dx)
    degreeValue_pitch = _convertRadianToDegree(radianValue=radianValue_pitch)

    if degreeValue_pitch < 0:
        # atan2의 값의 범위가 -pi~pi 까지 이기 때문에 음수 값이 나옴
        # 이를 해결하기 위하여 음수 값이 나올경우에 한하여
        # degree 단위 일때 +360, radian 단위 일때 +2pi 를 하여
        # 음수값을 양수값으로 변환한다(-pi~pi 의 범위가 0~2pi 범위로 변경하는 것임)
        # 반시계 방향의 회전각임
        degreeValue_pitch += 360
        #degreeValue_pitch = degreeValue_pitch % 360

    # 진북 방향으로 각도 변경
    degreeValue_pitch = _convert3AxisRotationDegree(degreeValue=degreeValue_pitch)

    # --------------------------------------------------------------------------------------
    # y축 고정하고 x-z 평면에 투영 => roll
    start_px = startPoint[0]
    start_py = startPoint[2]
    end_px = endPoint[0]
    end_py = endPoint[2]

    dy = end_py - start_py
    dx = end_px - start_px

    radianValue_roll = math.atan2(dy, dx)
    degreeValue_roll = _convertRadianToDegree(radianValue=radianValue_roll)

    if degreeValue_roll < 0:
        # atan2의 값의 범위가 -pi~pi 까지 이기 때문에 음수 값이 나옴
        # 이를 해결하기 위하여 음수 값이 나올경우에 한하여
        # degree 단위 일때 +360, radian 단위 일때 +2pi 를 하여
        # 음수값을 양수값으로 변환한다(-pi~pi 의 범위가 0~2pi 범위로 변경하는 것임)
        # 반시계 방향의 회전각임
        degreeValue_roll += 360
        #degreeValue_roll = degreeValue_roll % 360

    # 진북 방향으로 각도 변경
    degreeValue_roll = _convert3AxisRotationDegree(degreeValue=degreeValue_roll)

    # 최종 리턴 형태로 구성
    resultAllDegreeDict[Degree_Azimuth] = degreeValue_azimuth
    resultAllDegreeDict[Degree_Pitch] = degreeValue_pitch
    resultAllDegreeDict[Degree_Roll] = degreeValue_roll

    return resultAllDegreeDict

def getAllDegreeBlender(degreeValueDict):
    """
    * Blender에서 사용할 3축 회전각도 구하기
    - Created Date : 2021.10.22
    - Created by JSLee
    - dict key : RX | RY | RZ
    :param degreeValueDict: DTX에 저장된 3축 회전각도 dict
    :return: Blender에서 사용할 3축 회전각 결과 dict
    """
    # 최종 결과값 저장
    resultAllDegreeDict = dict()

    # azimuth : Blender Rotation Z 에 일력
    resultRotationZ = _convert3AxisRotationDegreeForBlender(degreeValue=degreeValueDict[Degree_Azimuth])
    # pitch : Blender Rotation X 에 입력
    resultRotationX = _convert3AxisRotationDegreeForBlender(degreeValue=degreeValueDict[Degree_Pitch])
    # roll : Blender Rotation Y 에 입력
    resultRotationY = _convert3AxisRotationDegreeForBlender(degreeValue=degreeValueDict[Degree_Roll])

    # 최종 리턴 형태로 구성
    resultAllDegreeDict[RotationX] = resultRotationX
    resultAllDegreeDict[RotationY] = resultRotationY
    resultAllDegreeDict[RotationZ] = resultRotationZ

    return resultAllDegreeDict

def getAllDegreeUnity(degreeValueDict):
    """
    * Unity에서 사용할 3축 회전각도 구하기
    - Created Date : 2021.10.22
    - Created by JSLee
    - dict key : RX | RY | RZ
    :param degreeValueDict: DTX에 저장된 3축 회전각도 dict
    :return: Blender에서 사용할 3축 회전각 결과 dict
    """
    # 최종 결과값 저장
    resultAllDegreeDict = dict()

    # azimuth : Unity Rotation Y 에 입력
    resultRotationY = _convert3AxisRotationDegreeForUnity(degreeValue=degreeValueDict[Degree_Azimuth])
    # pitch : Unity Rotation X 에 입력
    resultRotationX = _convert3AxisRotationDegreeForUnity(degreeValue=degreeValueDict[Degree_Pitch])
    # roll : Unity Rotation Z 에 입력
    resultRotationZ = _convert3AxisRotationDegreeForUnity(degreeValue=degreeValueDict[Degree_Roll])

    # 최종 리턴 형태로 구성
    resultAllDegreeDict[RotationX] = resultRotationX
    resultAllDegreeDict[RotationY] = resultRotationY
    resultAllDegreeDict[RotationZ] = resultRotationZ

    return resultAllDegreeDict











