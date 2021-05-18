import boto3
import matplotlib.image as img
import matplotlib.pyplot as plt
import cv2
import shutil
import glob

images = glob.glob('./*.jpg')
targets = ['./Hyeri/', './Mina/', './Hyewon/', './Minju/', './Yena/', './Yujin/', './Wonyoung/']
target = 'target.jpg'

def compare_faces(sourceFile, targetFile): 
    #sourceFile='source.jpg'
    #targetFile='target/target.jpg'
    client=boto3.client('rekognition')
    Simil = 0

    for i in targets:
        targetFile = i + target
        try:
            imageSource=open(sourceFile,'rb')
            imageTarget=open(targetFile,'rb')
        except:
            break;
        response=client.compare_faces(SimilarityThreshold=70, #저는 70으로 했습니다. (기존 80)
                                      SourceImage={'Bytes': imageSource.read()},
                                      TargetImage={'Bytes': imageTarget.read()})
        
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            Simil = faceMatch['Similarity']
            print('The face at ' +
                   str(position['Left']) + ' ' +
                   str(position['Top']) +
                   ' matches with ' + similarity + '% confidence')
            if Simil>90:
                imageSource.close()
                imageTarget.close()
                break;

        imageSource.close()
        imageTarget.close()
        if Simil > 90:
            src = './'
            dr = i
            shutil.move(src+sourceFile, dr+sourceFile)
            break
    return len(response['FaceMatches'])

def img_output():
    jpg = '/*.jpg'
    a = input("이름을 입력하세요: ")
    imgs = glob.glob('./' + a + jpg)
    fig = plt.figure()
    rows = 1
    cols = len(imgs)
    n = 1
    for i in imgs:
        img = cv2.imread(i)
        ax = fig.add_subplot(rows,cols,n)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.axis("off")
        n += 1

    plt.show()

def main():
    answer=0
    while 1:
        print("원하시는 기능을 선택하세요")
        print("1.이미지를 각 폴더로 정리")
        print("2.이름에 해당하는 이미지 출력")
        print("3.종료")
        answer = input()
        if answer=='1':
            for i in images:
                source_file= i
                target_file= 'target'
                face_matches=compare_faces(source_file, target_file)
        if answer=='2':
            img_output()

        if answer=='3':
            break;

if __name__ == "__main__":
    main()
