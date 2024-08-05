# This Python file uses the following encoding: utf-8
import sys
import time
import logging
import PySide6.QtGui

from picamera2 import Picamera2, Preview
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QTimer, QThread
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from support_functions import *

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QGroupBox, QLabel,
    QPushButton, QSizePolicy, QWidget)

from ui_form import Ui_MYAPP

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

class MYAPP(QWidget):
    """
    Hàm khởi tạo của MYAPP
    + Khởi tạo lớp cha (class QWidget)
    + Khởi tạo một đối tượng hiển thị Ui_MYAPP() bao gồm các phần tử được định nghĩa trong Ui_MYYAPP
    + Khởi tạo các biến trạng thái fullscreen_val, sensor_read_val
    + Khởi tạo picam2 là camera từ libcamera2, bật picam2.
    + Khởi tạo QPixmap để đọc ảnh dưới dạng QPixmap và hiển thị trên các đối tượng QLabel. 
    + Khởi tạo biến trạng thái camera_streaming_val, server_streaming_val, people_detection_val và biến đếm số lần nhấn nút FireWarning fire_waring_clicked_count
    + Khởi chạy các chương trình con chạy song song.
    + Kết nối các các hàm tới các nút nhấn.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MYAPP()
        self.ui.setupUi(self)
        self.fullscreen_val = True
        self.sensor_read_val = True
        # for CameraStreaming
        self.picam2 = Picamera2()
        self.picam2.start()
        self.pixmap = QPixmap("img.jpg")
        self.camera_streaming_val = True
        self.server_streaming_val = True
        self.people_detection_val = False
        self.fire_waring_value = False
        self.fire_waring_clicked_count = 0
        # self._SensorReading()
        # self._ServerStreaming()
        self._SensorReadingAndServerStreaming()
        self._ServerStreaming()
        # button connect
        self.ui.FullScreenButton.clicked.connect(self._FullSceenButtonAction)
        self.ui.RefreshButton.clicked.connect(self._RefreshButtonAction)
        self.ui.Camera_Control.clicked.connect(self._StartStopCameraButtonAction)
        self.ui.People_Detection.clicked.connect(self._StartStopPeopleDetection)
        self.ui.ServerSyncButton.clicked.connect(self._StartStopServerSync)
        self.ui.ClearNotiButton.clicked.connect(self._ClearAllNotification)
        self.ui.SetResetFireAlert_Button.clicked.connect(self._SetResetFireWaring)
        self.ui.RebootButton.clicked.connect(self._RebootButtonAction)
        self.ui.FireWarningBar.setVisible(False)
        # logger
        #TODO: create logger

    """
    Hàm đổi giá trị logic True thành False và ngược lại.
    NOTE: Vì một cái lý do nào đó mà toán tử ~ không hoạt động :<
    """
    def _not(self, var):
        if var == True:
            return False
        else:
            return True
        return -1

    """
    Hàm thay đổi chế độ hiển thị FullScreen/Maximized 
    """
    def _FullSceenButtonAction(self):
        FullSceenButtonAction(self)

    """
    Hàm thực hiện chức năng reboot.
    Hoạt động: Đầu tiên set trạng thái của <Notification2> để thông báo sẽ tắt sau 10s - không thể huỷ lệnh này, và sau đó đếm ngược.
    TODO: Chức năng hiển thị đang lỗi.
    """
    def _RebootButtonAction(self):
        self.ui.Notification2_Value.setText("Reboot after 10s - CANNOT CANCEL!")
        RebootButtonAction()

    """
    Hàm đặt lại <Notification1> và <Notification2>.
    """
    def _ClearAllNotification(self):
        if self.fire_waring_value == False:
            self.fire_waring_clicked_count = 0
            self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)
        self.ui.Notification1_Value.setText("<Notification 1>")
        self.ui.Notification2_Value.setText("<Notification 2>")

    """
    Hàm đặt lại <Notification1>, <Notification2> có chọn lựa.
    Code - Chọn <Notification1> hay <Notification2> hay cả 2 sẽ được đặt lại.
        + 01B:  Notification 1
        + 10B:  Notification 2
        + 11B:  Notification 1 & 2
    """
    def _ClearNotification(self, code = 3):
        if self.fire_waring_value == False:
            self.fire_waring_clicked_count = 0
            self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)
        if code & 1 != 0:
            self.ui.Notification1_Value.setText("<Notification 1>")
        if code & 2 != 0:
            self.ui.Notification2_Value.setText("<Notification 2>")

    """
    Hàm đặt giá trị cho <Notification1>, <Notification2> có chọn lựa.
    code - Chọn <Notification1> hay <Notification2> hay cả 2 sẽ được đặt lại.
        + 01B:  Notification 1
        + 10B:  Notification 2
        + 11B:  Notification 1 & 2
    msg  - Thông điệp được hiển thị:
        + Thông điệp cần ngắn gọn, dài quá sẽ bị cắt!
    """
    def _SetNotification(self, code = 1, msg = ""):
        if code & 1 != 0:
            self.ui.Notification1_Value.setText(msg)
        if code & 2 != 0:
            self.ui.Notification2_Value.setText(msg)

    """
    Hàm bật/tắt camera. Khi hàm được gọi, sẽ kiểm tra biến trạng thái self.camera_streaming_val:
    1.  Nếu self.camera_streaming_val = True nghĩa là đang bật:
            Thoát luồn đang chạy và dừng việc ghi hình ảnh.
            Hiển thị trạng thái lên UI.
    2.  Đão giá trị của biến trạng thái self.camera_streaming_val.
    3.  Nếu self.camera_streaming_val = True nghĩa là chưa bật:
            Bắt đầu lại picam2.
            Chờ khoảng 2 giây cho camera khởi động
            Gọi hàm để tạo lại luồng.
    """
    def _StartStopCameraButtonAction(self):
        if self.camera_streaming_val == True:
            self.thread1.exit()
            self.ui.Camera_Label.setText("Stopped camera streaming")
        self.camera_streaming_val = self._not(self.camera_streaming_val)
        if self.camera_streaming_val == True:
            self._CameraStreaming()

    """
    Hàm bật tắt tính năng nhận diện người
    TODO: Phát triển tính năng nhận diện người.
    """
    def _StartStopPeopleDetection(self):
        if self.people_detection_val == True:
            self.people_detection_val= False
        else:
            self.people_detection_val = True

        if self.people_detection_val == True:
            self._PeopleDetection()

    """
    Hàm thực hiện tính năng nhận diện người
    TODO: Phát triển tính năng nhận diện người.
    """
    def _PeopleDetection(self):
        PeopleDetection(self)

    """
    Hàm thực hiện công việc truyền hình ảnh ở một luồng (thread) khác.
    """
    def _CameraStreaming(self):
        #
        self.picam2.start()
        time.sleep(2) # warn-up time
        # Tạo luồng mới
        self.thread1 = QThread()
        # Tạo đối tượng worker
        self.CameraStreaming = CameraStreaming(self)
        # Di chuyển đối tượng worker vào luồng đã tạo
        self.CameraStreaming.moveToThread(self.thread1)
        # Kết nối hàm UpdateData của đối tượng worker đến luồng
        self.thread1.started.connect(self.CameraStreaming.UpdateData)
        # Kết nối hàm sẽ thực thi khi có tín hiệu finished từ Worker
        self.CameraStreaming.finished.connect(self.thread1.quit) # Thoát luồng
        self.CameraStreaming.finished.connect(self.CameraStreaming.deleteLater) # Xoá đối tượng
        self.thread1.finished.connect(self.thread1.deleteLater) # Xoá luồng
        # Bắt đầu chạy luồng
        self.thread1.start()

    """
    Hàm bật tắt đồng bộ máy chủ.
    1.  Đão giá trị biến trạng thái self.server_streaming_val.
    2.  Kiểm tra nếu self.server_streaming_val = True nghĩa là chưa bật
            Cập nhật trạng thái "Connected" trên UI
            Gọi chương trình khởi chạy,
        Nếu không (self.server_streaming_val = False):
            Cập nhật trạng thái "Disconnected" trên UI
        """
    def _StartStopServerSync(self):
        # if self.server_streaming_val == True:
        #    self.thread2.exit()
        self.server_streaming_val = self._not(self.server_streaming_val)
        # if self.server_streaming_val == True:
        #     self.ui.ServerConnection_Value.setText("Connected")
        #     self._ServerStreaming()
        # else:
        #     self.ui.ServerConnection_Value.setText("Disconnected")

    """
    Hàm thực hiện công việc đọc dữ liệu cảm biến và cập nhật lên UI ở luồng song song.
    """
    def _ServerStreaming(self):
        msg = """
            This function has been deleted after merged two classes 
            SensorReading and ServerStreaming into class SensorReadingAndServerStreaming 
            to prevent 'CRASHED' from simultaneously using GPIO BUS.
        """
        print("Called: _ServerStreaming()")
        print(msg)
        # self.ui.ServerConnection_Value.setText("Connected")
        # self.thread2 = QThread()
        # self.ServerStreaming = ServerStreaming(self)
        # self.ServerStreaming.moveToThread(self.thread2)
        # self.thread2.started.connect(self.ServerStreaming.UpdateData)
        # self.ServerStreaming.finished.connect(self.thread2.quit)
        # self.ServerStreaming.finished.connect(self.ServerStreaming.deleteLater)
        # self.thread2.finished.connect(self.thread2.deleteLater)
        # self.thread2.start()

    """
    Hàm đặt tên cho nút FireWarningButton.
        Tham số count - Cho biết số lần nút FireWarning được nhấn.
        Nếu biến count = 0: Hàm sẽ đặt tên FireWarningButton là "Set/Reset FireAlert".
        Ngược lại "Set/Reset FireAlert(count)".
    """
    def _SetFireWarningButtonTitle(self, count = 0):
        # "count = 0" means no countdown.
        if count == 0 :
            self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert");
        else:
            # "count > 0" meaning the button has been pressed count times.
            self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert({})".format(count))

    """
    Hàm bật tắt cảnh báo cháy thủ công.
    1.  Kiểm tra fire_waring_clicked_count - số lần nhấn nút đã đủ chưa, nếu chưa đủ chỉ cập nhật số lần nhấn.
    2.  Nếu đủ số lần nhấn nút, kiểm tra biến trạng thái báo cháy self.fire_waring_value 
            Nếu biến cảnh báo có giá trị True:
                Thay đổi trạng thái cảnh báo, xoá thông báo báo cháy.
            Ngược lại:
                Thay đổi trạng thái cảnh báo, hiển thị thông báo báo cháy.
                Gọi hàm thực hiện công việc cảnh báo cháy.
    """
    def _SetResetFireWaring(self):
        self.fire_waring_clicked_count = self.fire_waring_clicked_count + 1
        if self.fire_waring_clicked_count < 10:
            self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)
            return
        self.fire_waring_clicked_count = 0
        self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)

        if self.fire_waring_value == True:
            self.thread3.exit()
            self._ClearNotification(code=1)
        self.fire_waring_value = self._not(self.fire_waring_value)
        if self.fire_waring_value == True:
            self._FireWaring()

    """
    Hàm thực hiện công việc cảnh báo cháy ở luồng khác.
    """
    def _FireWaring(self):
        self.thread3 = QThread()
        self.FireWarning = FireWarning(self)
        self.FireWarning.moveToThread(self.thread3)
        self.thread3.started.connect(self.FireWarning.FireWarningAction)
        self.FireWarning.finished.connect(self.thread3.quit)
        self.FireWarning.finished.connect(self.FireWarning.deleteLater)
        self.thread3.finished.connect(self.thread3.deleteLater)
        self.thread3.start()

    """
    Hàm làm mới ngay lập tức giá trị của cảm biến.
    """
    def _RefreshButtonAction(self):
        self.ui.temp_value.setText(str(GetTemperature()) + " oC")
        self.sensor_read_val = ~ self.sensor_read_val
        if self.sensor_read_val == True:
            self._SensorReading()
        else:
            self.thread0.exit()

    """
        Hàm thực hiện công việc đọc giá trị cảm biến ở luồng khác.
    """
    def _SensorReading(self):
        msg = """
            This function has been deleted after merged two classes 
            SensorReading and ServerStreaming into class SensorReadingAndServerStreaming 
            to prevent 'CRASHED' from simultaneously using GPIO BUS.
        """
        print("Called: _SensorReading()")
        print(msg)
        # self.thread0 = QThread()
        # self.SensorReading = SensorReading(self)
        # self.SensorReading.moveToThread(self.thread0)
        # self.thread0.started.connect(self.SensorReading.UpdateData)
        # self.SensorReading.finished.connect(self.thread0.quit)
        # self.SensorReading.finished.connect(self.SensorReading.deleteLater)
        # self.thread0.finished.connect(self.thread0.deleteLater)
        # self.thread0.start()

    """
    Hàm thực hiện việc đọc cảm biến, cập nhật giá trị cảm biến lên UI, đồng bộ dữ liệu lên máy chủ ở luồng (thread) khác.
    """
    def _SensorReadingAndServerStreaming(self):
        self.thread0 = QThread()
        self.SensorReadingAndServerStreaming = SensorReadingAndServerStreaming(self)
        self.SensorReadingAndServerStreaming.moveToThread(self.thread0)
        self.thread0.started.connect(self.SensorReadingAndServerStreaming.Working)
        self.SensorReadingAndServerStreaming.finished.connect(self.thread0.quit)
        self.SensorReadingAndServerStreaming.finished.connect(self.SensorReadingAndServerStreaming.deleteLater)
        self.thread0.finished.connect(self.thread0.deleteLater)
        self.thread0.start()

    """
    Hàm huỷ, xoá các chân IO đã đặt.
    NOTE: IO được khai báo ở tập tin support_functions.py.
    """
    def __del__():
        IO.cleanup()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MYAPP()
    widget.showFullScreen()
    # widget.showNormal()
    sys.exit(app.exec())
