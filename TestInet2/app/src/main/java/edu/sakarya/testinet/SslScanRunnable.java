package edu.sakarya.testinet;

import android.content.Context;
import android.os.Handler;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import java.io.IOException;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Objects;
import javax.net.SocketFactory;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLSocket;

public class SslScanRunnable implements Runnable {


  private Context context;
  private Handler handler;
  private TextView textView;
  private ImageView imageView;
  private TextView secureStatus;

  private static boolean LOCK;
  private ArrayList<String> fakeHosts = new ArrayList<>();


  private final HashMap<String, String> hosts;

  private double totalPercent = 0.00;

  private SocketFactory socketFactory = HttpsURLConnection.getDefaultSSLSocketFactory();


  SslScanRunnable(Context context, Handler handler, TextView textView, ImageView imageView,
      TextView secureStatus) {
    this.context = context;
    this.handler = handler;
    this.textView = textView;
    this.imageView = imageView;
    this.secureStatus = secureStatus;

    hosts = new HashMap<>();
    initHosts();
  }

  private void initHosts() {

    hosts.put("google.com", "Google Trust Services");
    hosts.put("yandex.com", "Yandex Certification Authority");
    hosts.put("twitter.com", "DigiCert");
    hosts.put("facebook.com", "DigiCert");
    hosts.put("gmail.com", "Google Trust Services");
    hosts.put("eksisozluk.com", "Go Daddy");
    hosts.put("bing.com", "Microsoft");
    hosts.put("theguardian.com", "GlobalSign");
  }

  @Override
  public void run() {
    if (LOCK) {
      return;
    }
    LOCK = true;
    int correct = 0;
    fakeHosts.clear();
    for (String host : hosts.keySet()) {
      SSLSocket socket;
      try {
        int port = 443;
        socket = (SSLSocket) socketFactory.createSocket(host, port);
        socket.startHandshake();

        Certificate[] certs = socket.getSession().getPeerCertificates();
        Certificate cert = certs[0];

        String issuer = ((X509Certificate) cert).getIssuerDN().getName();
        if (issuer.contains(Objects.requireNonNull(hosts.get(host)))) {
          correct++;
        } else {
          fakeHosts.add(host);
        }

        double finalCorrect = correct;
        totalPercent = finalCorrect / hosts.size() * 100;
        handler.post(() -> textView.setText("%" + totalPercent));


      } catch (IOException e) {
        e.printStackTrace();
      }

      if (totalPercent != 100.00) {
        StringBuilder sentHost = new StringBuilder();
        for (int p = 0; p < fakeHosts.size(); p++) {
          sentHost.append(fakeHosts.get(p)).append(" ");

        }
        String sentNot = sentHost.toString();
        handler.post(() -> {
          imageView.setImageResource(R.drawable.ssl);
          if (!sentNot.equals("")) {
            Toast.makeText(this.context, sentNot, Toast.LENGTH_SHORT).show();
          }

          secureStatus.setText("Not Safe!");
        });
      } else {
        handler.post(() -> {
          imageView.setImageResource(R.drawable.ssl_ok);
          secureStatus.setText("Safe");
        });
      }

    }

    LOCK = false;

  }
}
