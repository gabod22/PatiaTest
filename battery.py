import wmi
from win32com.client import GetObject

w = wmi.WMI()


def wmi_get_battery_info():
    # for battery in w.query("select * from Win32_Battery"):
    #     print(battery.DesignCapacity)

    objWMI = GetObject("winmgmts:").InstancesOf("CIM_Battery")

    for obj in objWMI:
        if obj.Availability != None:
            print("Availability:" + str(obj.Availability))
        if obj.BatteryRechargeTime != None:
            print("BatteryRechargeTime:" + str(obj.BatteryRechargeTime))
        if obj.BatteryStatus != None:
            print("BatteryStatus:" + str(obj.BatteryStatus))
        if obj.Caption != None:
            print("Caption:" + str(obj.Caption))
        if obj.Chemistry != None:
            print("Chemistry:" + str(obj.Chemistry))
        if obj.ConfigManagerErrorCode != None:
            print("ConfigManagerErrorCode:" + str(obj.ConfigManagerErrorCode))
        if obj.ConfigManagerUserConfig != None:
            print("ConfigManagerUserConfig:" + str(obj.ConfigManagerUserConfig))
        if obj.CreationClassName != None:
            print("CreationClassName:" + str(obj.CreationClassName))
        if obj.Description != None:
            print("Description:" + str(obj.Description))
        if obj.DesignCapacity != None:
            print("DesignCapacity:" + str(obj.DesignCapacity))
        if obj.DesignVoltage != None:
            print("DesignVoltage:" + str(obj.DesignVoltage))
        if obj.DeviceID != None:
            print("DeviceID:" + str(obj.DeviceID))
        if obj.ErrorCleared != None:
            print("ErrorCleared:" + str(obj.ErrorCleared))
        if obj.ErrorDescription != None:
            print("ErrorDescription:" + str(obj.ErrorDescription))
        if obj.EstimatedChargeRemaining != None:
            print("EstimatedChargeRemaining:" + str(obj.EstimatedChargeRemaining))
        if obj.EstimatedRunTime != None:
            print("EstimatedRunTime:" + str(obj.EstimatedRunTime))
        if obj.ExpectedBatteryLife != None:
            print("ExpectedBatteryLife:" + str(obj.ExpectedBatteryLife))
        if obj.ExpectedLife != None:
            print("ExpectedLife:" + str(obj.ExpectedLife))
        if obj.FullChargeCapacity != None:
            print("FullChargeCapacity:" + str(obj.FullChargeCapacity))
        if obj.InstallDate != None:
            print("InstallDate:" + str(obj.InstallDate))
        if obj.LastErrorCode != None:
            print("LastErrorCode:" + str(obj.LastErrorCode))
        if obj.MaxRechargeTime != None:
            print("MaxRechargeTime:" + str(obj.MaxRechargeTime))
        if obj.Name != None:
            print("Name:" + str(obj.Name))
        if obj.PNPDeviceID != None:
            print("PNPDeviceID:" + str(obj.PNPDeviceID))
        if obj.PowerManagementCapabilities != None:
            print("PowerManagementCapabilities:" + str(obj.PowerManagementCapabilities))
        if obj.PowerManagementSupported != None:
            print("PowerManagementSupported:" + str(obj.PowerManagementSupported))
        if obj.SmartBatteryVersion != None:
            print("SmartBatteryVersion:" + str(obj.SmartBatteryVersion))
        if obj.Status != None:
            print("Status:" + str(obj.Status))
        if obj.StatusInfo != None:
            print("StatusInfo:" + str(obj.StatusInfo))
        if obj.SystemCreationClassName != None:
            print("SystemCreationClassName:" + str(obj.SystemCreationClassName))
        if obj.SystemName != None:
            print("SystemName:" + str(obj.SystemName))
        if obj.TimeOnBattery != None:
            print("TimeOnBattery:" + str(obj.TimeOnBattery))
        if obj.TimeToFullCharge != None:
            print("TimeToFullCharge:" + str(obj.TimeToFullCharge))
        print("")
        print("########")
        print("")


wmi_get_battery_info()
