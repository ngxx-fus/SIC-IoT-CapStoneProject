# This Python file uses the following encoding: utf-8
import sys
import time
import logging
import PySide6.QtGui

from picamera2 import Picamera2, Preview
from libcamera import Transform
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
    Main class: MYAPP
    """

    def __init__(self, parent=None):
        """
        Hàm khởi tạo của MYAPP
        + Khởi tạo lớp cha (class QWidget)
        + Khởi tạo một đối tượng hiển thị Ui_MYAPP() bao gồm các phần tử được định nghĩa trong Ui_MYYAPP
        + Khởi tạo các biến trạng thái fullscreen_val, sensor_read_val
        + Khởi tạo picam2 là camera từ libcamera2, bật picam2.
        + Khởi tạo QPixmap để đọc ảnh dưới dạng QPixmap và hiển thị tMYAPPrên các đối tượng QLabel.
        + Khởi tạo biến trạng thái camera_streaming_val, server_streaming_val, people_detection_val, self.auto_stop_fire_alert và biến đếm số lần nhấn nút FireWarning fire_waring_clicked_count
        + Khởi chạy các chương trình con chạy song song.
        + Kết nối các các hàm tới các nút nhấn.
        """
        super().__init__(parent)
        self.ui = Ui_MYAPP()
        self.ui.setupUi(self)
        self.fullscreen_val = True
        self.sensor_read_val = True
        # for CameraStreaming
        self.picam2 = Picamera2()
        # config = self.picam2.create_still_configuration(transform=Transform(hflip=True))
        # self.picam2.configure(config)
        self.picam2.start()
        self.pixmap = QPixmap("./Imgs/img.jpg")
        self.light_switch_value = False
        self.fire_switch_value  = False
        self.camera_streaming_val = True
        self.server_streaming_val = False
        self.people_detection_val = False
        self.fire_waring_value = False
        self.auto_start_fire_alert = False
        # TODO: Remove soon
        self.auto_stop_fire_alert = False
        self.fire_waring_clicked_count = 0
        self._CameraStreaming()
        # self._SensorReading()
        # self._ServerStreaming()
        self._SensorReadingAndServerStreaming()
        # button connect
        self.ui.FullScreenButton.clicked.connect(self._FullSceenButtonAction)
        self.ui.RefreshButton.clicked.connect(self._RefreshButtonAction)
        self.ui.Camera_Control.clicked.connect(self._StartStopCameraButtonAction)
        self.ui.People_Detection.clicked.connect(self._StartStopPeopleDetection)
        self.ui.ServerSyncButton.clicked.connect(self._StartStopServerSync)
        self.ui.ClearNotiButton.clicked.connect(self._ClearAllNotification)
        self.ui.SetResetFireAlert_Button.clicked.connect(self._FireWaringButtonAction)
        self.ui.RebootButton.clicked.connect(self._RebootButtonAction)
        self.ui.AutoStartFireAlert.clicked.connect(self._SetAutoStartFireAlert)
        self.ui.LightButton.clicked.connect(self._SetResetLightState)
        self.ui.FireWarningBar.setVisible(False)
        self._SetNotification(1, "Auto Set Fire Alarm: {}".format(self.auto_start_fire_alert))
        # logger
        #TODO: create logger

    def _not(self, var):
        """
        Hàm đổi giá trị logic True thành False và ngược lại.
        NOTE: Vì một cái lý do nào đó mà toán tử ~ không hoạt động :<
        """
        if var == True:
            return False
        else:
            return True
        return -1

    def _FullSceenButtonAction(self):
        """
        Hàm thay đổi chế độ hiển thị FullScreen/Maximized
        """
        FullSceenButtonAction(self)

    def _SetAutoStartFireAlert(self):
        """
        Hàm đão giá trị của biến trạng thái self.auto_start_fire_alert.
        Biến self.auto_start_fire_alert quyết định xem hệ thống có tự động kích hoạt cảnh báo hay không.
        """
        self.auto_start_fire_alert = self._not(self.auto_start_fire_alert)
        self._SetNotification(2, "Auto set fire alarm: {}".format(self.auto_start_fire_alert))

    def _SetAutoStopFireAlert(self):
        """
        Hàm đão giá trị của biến trạng thái self.auto_stop_fire_alert.
        Biến self.auto_stop_fire_alert quyết định xem hệ thống có tự động bất hoạt cảnh báo hay không.
        """
        self.auto_stop_fire_alert = self._not(self.auto_stop_fire_alert)
        self._SetNotification(2, "Auto STOP Fire Alert: {}".format(self.auto_stop_fire_alert))

    def _RebootButtonAction(self):
        """
        Hàm thực hiện chức năng reboot.
        """
        RebootButtonAction(self)

    def _SetResetLightState(self):
        self.light_switch_value = self._not(self.light_switch_value)

    def _ClearAllNotification(self):
        """
        Hàm đặt lại <Notification1> và <Notification2>.
        """
        self.ui.Notification1_Value.setText("<Notification 1>")
        self.ui.Notification2_Value.setText("<Notification 2>")

    def _ClearNotification(self, code = 3):
        """
        Hàm đặt lại <Notification1>, <Notification2> có chọn lựa.
        Code - Chọn <Notification1> hay <Notification2> hay cả 2 sẽ được đặt lại.
            + 01B:  Notification 1
            + 10B:  Notification 2
            + 11B:  Notification 1 & 2
        """
        if code & 1 != 0:
            self.ui.Notification1_Value.setText("<Notification 1>")
        if code & 2 != 0:
            self.ui.Notification2_Value.setText("<Notification 2>")

    def _SetNotification(self, code = 1, msg = ""):
        """
        Hàm đặt giá trị cho <Notification1>, <Notification2> có chọn lựa.
        code - Chọn <Notification1> hay <Notification2> hay cả 2 sẽ được đặt lại.
            + 01B:  Notification 1
            + 10B:  Notification 2
            + 11B:  Notification 1 & 2
        msg  - Thông điệp được hiển thị:
            + Thông điệp cần ngắn gọn, dài quá sẽ bị cắt!
        """
        if code & 1 == 1:
            self.ui.Notification1_Value.setText(msg)
        if code & 2 == 2:
            self.ui.Notification2_Value.setText(msg)

    def _StartStopCameraButtonAction(self):
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
        self.ui.Camera_Control.setEnabled(False)
        if self.camera_streaming_val == True:
            self.thread1.exit()
            self.ui.Camera_Label.setText("Stopped camera streaming")
        self.camera_streaming_val = self._not(self.camera_streaming_val)
        if self.camera_streaming_val == True:
            self._CameraStreaming()
        self.ui.Camera_Control.setEnabled(True)

    def _StartStopPeopleDetection(self):
        """
        Hàm bật tắt tính năng nhận diện người
        TODO: Phát triển tính năng nhận diện người.
        """
        if self.people_detection_val == True:
            self.people_detection_val= False
        else:
            self.people_detection_val = True

        if self.people_detection_val == True:
            self._PeopleDetection()

    def _PeopleDetection(self):
        """
        Hàm thực hiện tính năng nhận diện người
        TODO: Phát triển tính năng nhận diện người.
        """
        PeopleDetection(self)

    def _CameraStreaming(self):
        """
        Hàm thực hiện công việc truyền hình ảnh ở một luồng (thread) khác.
        """
        # if hasattr(self, "thread1") == True:
        #     return
        #
        self.picam2.start()
        time.sleep(1) # warn-up time
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

    def _StartStopServerSync(self):
        """
        Hàm bật tắt đồng bộ máy chủ.
        """
        self.server_streaming_val = self._not(self.server_streaming_val)


    def _SetFireWarningButtonTitle(self, count = 0):
        """
        Hàm đặt <tựa đề> cho nút FireWarningButton.
            Tham số count - Cho biết số lần nút FireWarning được nhấn.
            Nếu biến count = 0: Hàm sẽ đặt tên FireWarningButton là "Set/Reset FireAlert".
            Ngược lại "Set/Reset FireAlert(count)".
        """
        # "count = 0" means no countdown.
        if count == 0 :
            self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert");
        else:
            # "count > 0" meaning the button has been pressed count times.
            self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert({})".format(count))

    def _FireWaringButtonAction(self):
        """
        Hàm quản lý nút nhấn kích hoạt cảnh báo cháy thủ công.
        """
        if self.fire_waring_clicked_count < 9:
            self.fire_waring_clicked_count = self.fire_waring_clicked_count + 1
            self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)
            return
        self.fire_waring_clicked_count = 0
        self._SetFireWarningButtonTitle(self.fire_waring_clicked_count)
        self.fire_switch_value = self._not(self.fire_switch_value)

    def _SetResetFireWaring(self, priority_flag = False, priority_setter = False):
        """
        Hàm thực hiện việc bật tắt cảnh báo cháy.
        Chế độ ưu tiên:
        + Đặt biến giá trị ngay lập tức fire_waring_value theo giá trị đặt trước.
        Chế độ bình thường:
        + Lật trạng thái.
        Chú ý:
        + Cả hai chế độ điều có bảo vệ việc tạo lại luồng.
        """
        # Priority mode
        if priority_flag == True:
            # print("""[INFO] MYAPP._SetResetFireWaring: Running priority mode...""")
            if priority_setter == True:
                # print("[INFO] MYAPP._SetResetFireWaring: Set")
                self.fire_waring_value = True
                self._FireWaring()
                return
            elif priority_setter == False:
                # print("[INFO] MYAPP._SetResetFireWaring: Reset")
                if hasattr(self, "thread3") == True:
                    self.thread3.exit()
                    self.fire_waring_value = False
                    self._ClearNotification(code=1)
                    return
            # else:
                # print("[INFO] MYAPP._SetResetFireWaring: Change to normal mode.")

        # Normal mode
        # print("""[INFO] MYAPP._SetResetFireWaring: Running normal mode...""")
        if self.fire_waring_value == True:
            if hasattr(self, "thread3") == True:
                # print("[INFO] MYAPP._SetResetFireWaring: Reset")
                self.thread3.exit()
                self._ClearNotification(code=1)
        
        self.fire_waring_value = self._not(self.fire_waring_value)
        
        if self.fire_waring_value == True:
            # print("[INFO] MYAPP._SetResetFireWaring: Set")
            self.fire_waring_value = True
            self._FireWaring()

    def _FireWaring(self):
        """
        Hàm thực hiện công việc cảnh báo cháy ở luồng khác.
        """
        # print("[INFO] MYAPP._FireWaring: Creating thread3!")
        # if hasattr(self, "thread3") == True:
        #     print("[INFO] MYAPP._FireWaring: thread3 exist -> Abort!")
        #     return
        self.thread3 = QThread()
        self.FireWarning = FireWarning(self)
        self.FireWarning.moveToThread(self.thread3)
        self.thread3.started.connect(self.FireWarning.FireWarningAction)
        self.FireWarning.finished.connect(self.thread3.quit)
        self.FireWarning.finished.connect(self.FireWarning.deleteLater)
        self.thread3.finished.connect(self.thread3.deleteLater)
        self.thread3.start()

    def _RefreshButtonAction(self):
        """
        Hàm làm mới ngay lập tức giá trị của cảm biến.
        Đồng thời quyết định việc cập nhật giá trị lên UI. (Lật trạng thái.)
        Có khả năng gây CRASHED vì sử dụng chung BUS.
        """
        Sensor = self.SensorReadingAndServerStreaming.Sensor
        Sensor.Read()
        self.ui.temp_value.setText(ValueFormat(Sensor.Temp, suffix=" oC"))
        self.ui.humid_value.setText(ValueFormat(Sensor.Humid, suffix=" %"))
        self.ui.GAS_value.setText(ValueFormat(Sensor.GAS))
        self.sensor_read_val = self._not(self.sensor_read_val)

    def _SensorReadingAndServerStreaming(self):
        """
        Hàm thực hiện việc đọc cảm biến, cập nhật giá trị cảm biến lên UI, đồng bộ dữ liệu lên máy chủ ở luồng (thread) khác.
        """
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
    def __del__(self):
        IO.cleanup()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MYAPP()
    widget.showFullScreen()
    # widget.showNormal()
    sys.exit(app.exec())
