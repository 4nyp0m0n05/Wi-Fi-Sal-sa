package edu.sakarya.salsa;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import android.content.Context;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.internal.util.reflection.FieldSetter;
import org.mockito.runners.MockitoJUnitRunner;


@RunWith(MockitoJUnitRunner.class)
public class ExampleUnitTest {

  @Mock
  Context mockContext;

  @InjectMocks
  WifiService wifiService;

  @Mock
  WifiManager wifiManager;

  @Mock
  ScanResult sr1;

  @Mock
  ScanResult sr2;

  @Mock
  ScanResult sr3;

  @Spy
  ArrayList<ScanResult> scanResults;

  @Before
  public void init() throws NoSuchFieldException {
    new FieldSetter(sr1, ScanResult.class.getDeclaredField("SSID")).set("SAU-NET");
    new FieldSetter(sr1, ScanResult.class.getDeclaredField("capabilities"))
        .set("[WPA-PSK-CCMP+TKIP][WPA2-PSK-CCMP+TKIP][ESS]");

    new FieldSetter(sr2, ScanResult.class.getDeclaredField("SSID")).set("SAU-NET1");
    new FieldSetter(sr2, ScanResult.class.getDeclaredField("capabilities"))
        .set("[WPA-PSK-CCMP+TKIP][WPA2-PSK-CCMP+TKIP][ESS]");

    new FieldSetter(sr3, ScanResult.class.getDeclaredField("SSID")).set("SAU-NET");
    new FieldSetter(sr3, ScanResult.class.getDeclaredField("capabilities")).set("[OPN]");

    scanResults.add(sr1);
    scanResults.add(sr2);
    scanResults.add(sr3);

    when(wifiManager.getScanResults()).thenReturn(scanResults);
  }


  @Test
  public void addition_isCorrect() {

    ScanResult scanResult = checkWifis();
    assert scanResult != null;
    assertEquals("SAU-NET", scanResult.SSID);
    verify(wifiManager).getScanResults();
  }

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
}