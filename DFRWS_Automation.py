import face_recognition
from PIL import Image, ImageDraw
import os

def save_child_faces_from_folder(input_folder, output_folder):
    # 입력 폴더 경로 확인
    if not os.path.isdir(input_folder):
        print(f'Error: Input folder "{input_folder}" does not exist.')
        return
    
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # 입력 폴더 내의 모든 파일에 대해 처리
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            
            try:
                # 이미지 불러오기
                image = face_recognition.load_image_file(image_path)
                
                # 얼굴 위치 및 특징 추출
                face_locations = face_recognition.face_locations(image)
                face_landmarks_list = face_recognition.face_landmarks(image)
                
                # 연령 정보가 18세 이하인 경우의 얼굴만 저장
                for (top, right, bottom, left), face_landmarks in zip(face_locations, face_landmarks_list):
                    # 추출된 얼굴 이미지를 이용하여 연령 추정하기
                    face_image = image[top:bottom, left:right]
                    age_predictions = face_recognition.face_ageitgey(face_image)
                    age = age_predictions[0]
                    
                    # 연령이 18세 이하인 경우에만 저장
                    if age <= 18:
                        # 이미지 파일명 생성
                        output_filename = f'child_face_{filename}_{top}_{right}_{bottom}_{left}'
                        output_filepath = os.path.join(output_folder, output_filename)
                        
                        # 이미지 저장
                        pil_image = Image.fromarray(face_image)
                        pil_image.save(output_filepath)
                        
                        print(f'Saved face with age {age} from {filename} to {output_filepath}')
            
            except Exception as e:
                print(f'Error processing {filename}: {str(e)}')

# 예시: 입력 폴더와 출력 폴더 설정
input_folder = 'Images/B/brev'
output_folder = 'Please'

# 함수 호출
save_child_faces_from_folder(input_folder, output_folder)