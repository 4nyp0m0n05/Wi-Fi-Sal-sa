package edu.sakarya.salsa;

import android.app.ActivityManager;
import android.app.ActivityManager.RunningServiceInfo;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

  private WifiManager wifiManager;
  private ListView listView;
  private Button buttonScan;
  private Button serviceBtn;
  private int size = 0;
  private List<ScanResult> results;
  private ArrayList<String> arrayList = new ArrayList<>();
  private ArrayAdapter adapter;

  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    buttonScan = findViewById(R.id.scanBtn);
    buttonScan.setOnClickListener(view -> scanWifi());
    serviceBtn = findViewById(R.id.startServiceBtn);

    listView = findViewById(R.id.wifiList);
    wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);

    if (!wifiManager.isWifiEnabled()) {
      Toast.makeText(this, "WiFi is disabled ... We need to enable it", Toast.LENGTH_LONG).show();
      wifiManager.setWifiEnabled(true);
    }

    isMyServiceRunning();

    adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, arrayList);
    listView.setAdapter(adapter);
    scanWifi();
  }

  private boolean isMyServiceRunning() {
    ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
    for (RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
      if (WifiService.class.getName().equals(service.service.getClassName())) {
        serviceBtn.setText("Stop Service");
        serviceBtn.setOnClickListener(view -> {
          stopService(new Intent(this, WifiService.class));
          isMyServiceRunning();
        });
        return true;
      }
    }
    serviceBtn.setText("Start Service");
    serviceBtn.setOnClickListener(view -> {
      startService(new Intent(this, WifiService.class));
      isMyServiceRunning();
    });
    return false;
  }


  private void scanWifi() {
    arrayList.clear();
    registerReceiver(wifiReceiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    wifiManager.startScan();
    Toast.makeText(this, "Scanning WiFi ...", Toast.LENGTH_SHORT).show();
  }

  BroadcastReceiver wifiReceiver = new BroadcastReceiver() {
    @Override
    public void onReceive(Context context, Intent intent) {
      results = wifiManager.getScanResults();
      unregisterReceiver(this);

      for (ScanResult scanResult : results) {
        arrayList.add(scanResult.SSID + " - " + scanResult.capabilities);
        adapter.notifyDataSetChanged();
      }
    }
  };
}