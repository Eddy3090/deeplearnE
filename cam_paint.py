def get_heatmap(cam, img):
    cam -= np.min(cam)
    cam /= np.max(cam)
    cam = np.square(cam)

    img = img/2+0.5

    cam = cv2.resize(cam, img.shape)
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    # heatmap[np.where(cam < 0.2)] = 0
    img = img[:,:,np.newaxis]
    img_3chn = np.concatenate((img ,img ,img),axis=-1)
    heatmap = np.float64(heatmap)/255.
    img_cam = heatmap * 0.3 + img_3chn*0.7
    # img4 = cv2.addWeighted(np.float64(heatmap), 0.4, img2, 0.6, 0)    
    return heatmap, img_cam