package edu.sakarya.testinet.wificontroller;


import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Handler;
import android.widget.Switch;
import android.widget.TextView;

/**
 * Receives wifi changes and creates a notification when wifi connects to a network,
 * displaying the SSID and MAC address.
 * <p>
 * Put the following in your manifest
 * <p>
 * <receiver android:name=".WifiReceiver" android:exported="false" >
 * <intent-filter>
 * <action android:name="android.net.wifi.WIFI_STATE_CHANGED" />
 * </intent-filter>
 * </receiver>
 * <service android:name=".WifiReceiver$WifiActiveService" android:exported="false" />
 * <p>
 * To activate logging use: adb shell setprop log.tag.WifiReceiver VERBOSE
 */
public class WifiReceiver extends BroadcastReceiver {



    private Switch aSwitch;

    public WifiReceiver(){

    }

    public WifiReceiver(Switch aSwitch) {
        this.aSwitch = aSwitch;
    }

    @Override
    public void onReceive(final Context context, final Intent intent) {
        int wifiStateExtra = intent.getIntExtra(WifiManager.EXTRA_WIFI_STATE,
                WifiManager.WIFI_STATE_UNKNOWN);

        switch (wifiStateExtra) {
            case WifiManager.WIFI_STATE_ENABLED:
                aSwitch.setChecked(true);
                break;
            case WifiManager.WIFI_STATE_DISABLED:
                aSwitch.setChecked(false);
                break;
        }

    }

}
