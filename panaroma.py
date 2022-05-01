import cv2 
import depthai as dai

#create a pipeline
pipeline = dai.Pipeline()

#define the source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

#properties

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1920, 1080)
camRgb.setVideoSize(1280, 720)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

#Linking
camRgb.video.link(xoutVideo.input)

with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
    img_count=0
    frames = []
    while True:
        videoIn = video.get()
        output = videoIn.getCvFrame()
        #Get BGR from NV12 encoded video frame to show with opencv
        cv2.imshow("video", output)

        
        if cv2.waitKey(1) == ord('c'):
            frames.append(output)
            img_count +=1
            print(len(frames))
        if cv2.waitKey(1) == ord('p'):
            print('Creating Panaroma')
            if img_count < 2:
                print('click more pictures for a panaroma')
            else:
                stitcher=cv2.Stitcher.create()
                code,panaroma =stitcher.stitch(frames)
                if code != cv2.STITCHER_OK:
                    print("stitching not successful")
                else:
                    print('Your Panorama is ready!!!')
                    cv2.imshow('final result',panaroma)
                    cv2.imwrite('panaroma.jpg', panaroma)
        
        if cv2.waitKey(1) == ord('q'):
            break