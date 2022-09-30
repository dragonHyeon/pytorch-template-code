# MovementsDTXSL
- 시설물 도면 데이터 추출 모듈
___
### 프로그램 실행 방법 인자 설명
- entry point
  - AppPath/Main/MainDTX.py
  - parameter
    - --running_mode : 'deploy', 'dev'
      - required
      - 입력값
        - deploy : 운영 모드
        - dev : 개발 모드
    - --dxf_path_or_dir : DXF 파일 경로 또는 해당 디렉터리 (str)
      - 입력값 예시
        - ex) ./RES
    - --output_dir : 결과물 저장될 디렉터리 (str)
      - 입력값 예시
        - ex) ./DATA
    - --vis_mode : 시각화 여부 (bool)
      - 입력값 예시
        - ex) True