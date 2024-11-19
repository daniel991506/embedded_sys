from bluepy.btle import Scanner, Peripheral, DefaultDelegate, BTLEException, UU>
import time


# 自訂通知委派，用來處理收到的 Notification/Indication
class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    def handleNotification(self, cHandle, data):
        print(f"收到通知: Handle={cHandle}, Data={data.decode('utf-8', 'ignore'>


# 掃描 BLE 裝置
def scan_devices():
    scanner = Scanner()
    print("正在掃描 BLE 裝置...")
    devices = scanner.scan(10.0)


    addr_list = []
    for i, dev in enumerate(devices):
name = dev.getValue(9) or "未知裝置"
        print(f"{i}: {name} - {dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB")
        addr_list.append(dev.addr)


    return addr_list


# 連接到 BLE Peripheral
def connect_device(address, addr_type='random'):
    try:
        print(f"正在連接裝置: {address}...")
        dev = Peripheral(address, addrType=addr_type)
        dev.setDelegate(NotificationDelegate())  # 設定通知處理
        print("連接成功！")
        return dev
    except BTLEException as e:
        print(f"連接失敗: {e}")
        return None




# 探索服務與特徵值，並啟用 Notification/Indication
def explore_and_enable_notifications(dev):
    print("探索裝置的服務與特徵值...")
    for svc in dev.services:
        print(f"Service: {svc.uuid}")
        for char in svc.getCharacteristics():
            print(f"  Characteristic: {char.uuid}, Properties: {char.properties>


            # 啟用 Notification 或 Indication（根據屬性）
            if "NOTIFY" in char.propertiesToString() and char.uuid=='0000fff4-0>
                try:
                    cccd_handle = char.getHandle()  # CCCD Handle
                    # 根據需求設為 Notification (0x01) 或 Indication (0x02)
                    value = b'\x01\x00' if "NOTIFY" in char.propertiesToString(>
                    dev.writeCharacteristic(cccd_handle, value, withResponse=Tr>
                    print(f"    已啟用: {char.uuid} (CCCD Handle: {cccd_handle}>
                except Exception as e:
                    print(f"    無法啟用通知: {e}")


# 等待 Notification/Indication
def wait_for_notifications(dev):
    print("等待通知...(按 Ctrl+C 結束)")
    try:
        while True:
            if dev.waitForNotifications(1.0):
                print("收到並處理通知")
            else:
                print("無通知")
    except KeyboardInterrupt:
        print("結束通知監聽")


# 主程式流程
if __name__ == "__main__":
    ddr_list = scan_devices()


    try:


        choice = int(input("請輸入要連接的裝置編號: "))
        target_addr = ddr_list[choice]
    except (IndexError, ValueError):
        print("輸入無效，請重新執行並輸入正確的裝置編號。")
        exit(1)


    dev = connect_device(target_addr)
    if dev:
        explore_and_enable_notifications(dev)
        wait_for_notifications(dev)


        print("斷開連接...")
        dev.disconnect()
        print("已斷開連接")
    else:
        print("無法連接裝置，請檢查裝置狀態或重新掃描。")