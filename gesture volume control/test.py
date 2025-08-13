import cv2

apis = [("DSHOW", cv2.CAP_DSHOW), ("MSMF", cv2.CAP_MSMF)]
indices = range(0, 6)

cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Preview", 640, 360)

selected = None
for api_name, api in apis:
    for i in indices:
        cap = cv2.VideoCapture(i, api)
        if not cap.isOpened():
            continue
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        print(f"Testing index {i} with {api_name}...")

        ok, frame = cap.read()
        if not ok:
            cap.release(); continue

        while True:
            ok, frame = cap.read()
            if not ok: break
            cv2.putText(frame, f"{api_name} index {i}  (S=select, N=next, ESC=quit)",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.imshow("Preview", frame)
            k = cv2.waitKey(30) & 0xFF
            if k == 27: cap.release(); cv2.destroyAllWindows(); raise SystemExit()
            if k in (ord('s'), ord('S')): selected = (i, api); break
            if k in (ord('n'), ord('N')): break

        cap.release()
        if selected: break
    if selected: break

cv2.destroyAllWindows()
if not selected:
    raise SystemExit("No camera selected. Make sure DroidCam Client is connected to the phone.")

idx, api = selected
print(f"Using {idx} with {'DSHOW' if api==cv2.CAP_DSHOW else 'MSMF'}")

# Final preview using the chosen device
cap = cv2.VideoCapture(idx, api)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

title = "DroidCam (virtual)"
cv2.namedWindow(title, cv2.WINDOW_NORMAL)
cv2.resizeWindow(title, 640, 360)

while True:
    ok, frame = cap.read()
    if not ok: break
    cv2.imshow(title, frame)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release(); cv2.destroyAllWindows()
