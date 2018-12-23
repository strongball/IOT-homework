import cv2

frame = cv2.imread("./storge/shape.jpg")
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
_,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20)
print(circles)
for c in contours:
    peri = cv2.arcLength(c, True)
    if peri < 50:
        continue
    approx = cv2.approxPolyDP(c,0.1*peri,True)

    ct = len(approx)
    if ct <= 5 and ct > 2:
        cv2.drawContours(frame,[approx],-1,(0,0,255),3)

cv2.imshow("img", frame)

cv2.waitKey(0)
cv2.destroyAllWindows()