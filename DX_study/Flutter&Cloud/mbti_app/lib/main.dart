import 'package:flutter/material.dart';
import 'package:mbti_app/test_page.dart';

void main() {
  runApp(MbtiApp());
}

class MbtiApp extends StatelessWidget {
  const MbtiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MbtiTestPage(),
    );
  }
}
