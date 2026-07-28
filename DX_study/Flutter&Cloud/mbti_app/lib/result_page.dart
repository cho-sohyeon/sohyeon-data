import 'package:flutter/material.dart';

class ResultPage extends StatelessWidget {
  final String result;

  const ResultPage({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('MBTI 결과'),
      ),
      body: Center(
        child: Text(
          '당신의 MBTI 유형은 $result 입니다.',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
