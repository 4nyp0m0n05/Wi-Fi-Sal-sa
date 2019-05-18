package edu.sakarya.salsa;

import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.IBinder;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationCompat.BigTextStyle;
import androidx.core.app.NotificationManagerCompat;
import java.util.List;

public class WifiService extends Service {

  private WifiManager wifiManager;

  public WifiService() {
  }

  BroadcastReceiver wifiReceiver = new BroadcastReceiver() {
    @Override
    public void onReceive(Context context, Intent intent) {
      ScanResult scanResult = checkWifis();
      if (scanResult == null) {
        sendOk();
      } else {
        sendWarning(scanResult.SSID);
      }
    }
  };

  private ScanResult checkWifis() {
    List<ScanResult> scanResults = wifiManager.getScanResults();

    for (int i = 0; i < scanResults.size(); i++) {
      ScanResult scanResult = scanResults.get(i);

      for (int j = 0; j < scanResults.size(); j++) {
        ScanResult scanResult1 = scanResults.get(j);

        if (scanResult1.SSID.equals(scanResult.SSID) && !scanResult1.capabilities
            .equals(scanResult.capabilities)) {
          return scanResult;
        }
      }

    }
    return null;
  }

  @Override
  public IBinder onBind(Intent intent) {

    return null;
  }

  @Override
  public void onCreate() {
    wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
    registerReceiver(wifiReceiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    wifiManager.startScan();
  }

  @Override
  public void onDestroy() {
    super.onDestroy();
    unregisterReceiver(wifiReceiver);
  }

  public void sendWarning(String ssid) {
    NotificationCompat.Builder builder = new NotificationCompat.Builder(this, "123qwe")
        .setContentTitle("Warning")
        .setSmallIcon(R.drawable.ic_warning)
        .setStyle(new NotificationCompat.BigTextStyle()
            .bigText("This WiFi is dangerous : " + ssid))
        .setPriority(NotificationCompat.PRIORITY_DEFAULT);

    NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);

    // notificationId is a unique int for each notification that you must define
    notificationManager.notify(123, builder.build());
  }

  public void sendOk() {
    NotificationCompat.Builder builder = new NotificationCompat.Builder(this, "123qwe")
        .setContentTitle("Safe WiFi")
        .setSmallIcon(R.drawable.ic_security)
        .setStyle(new BigTextStyle().bigText("There is no threat on WiFi. You are safe for now."))
        .setPriority(NotificationCompat.PRIORITY_DEFAULT);

    NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);

    // notificationId is a unique int for each notification that you must define
    notificationManager.notify(124, builder.build());
  }
}
