import 'package:flutter/material.dart';
import 'package:mbti_app/answer_model.dart';
import 'package:mbti_app/question_box.dart';
import 'package:mbti_app/question_model.dart';
import 'package:mbti_app/result_page.dart';

class MbtiTestPage extends StatelessWidget {
  const MbtiTestPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(),
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Expanded(
            child: buildListView(),
          ),

          // 결과 버튼
          buildResultButton(context),
        ],
      ),
    );
  }

  ListView buildListView() {
    return ListView(
      children: [
        // 녹색 박스 그리기
        buildHeader(),

        //질문 박스들 그리기
        for (var question in questions) QuestionBox(question: question),
      ],
    );
  }

  Widget buildResultButton(BuildContext context) {
    return GestureDetector(
      onTap: () {
        final String mbti = calculateMBTI(questions, allSelectedAnswers.values.toList());
        final route = MaterialPageRoute(
          builder: (context) {
            return ResultPage(result: mbti);
          },
        );
        Navigator.push(context, route);
      },
      child: Container(
        height: 56,
        decoration: BoxDecoration(
          color: Color(0xFF863BA6),
        ),
        child: Center(
          child: Text(
            "결과 보기",
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }

  Container buildHeader() {
    return Container(
      color: Color(0xFF33A474),
      padding: EdgeInsets.all(20),
      child: Column(
        children: [
          Text(
            "MBTI 테스트",
            style: TextStyle(
              color: Colors.white,
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),

          Text(
            "MBTI Testing App",
            style: TextStyle(
              color: Colors.white,
              fontSize: 14,
            ),
          ),

          Container(height: 1, color: Colors.white10),

          //가이드박스1
          buildGuideBox("assets/header_icon1.png", "자신의 성격 유형을 확인할 수 있도록 솔직하게 답변해주세요."),

          //가이드박스2
          buildGuideBox("assets/header_icon2.png", "자신의 성격 유형이 삶의 여러 영역에 어떤 영향을 미치는지 알아보세요."),

          //가이드박스3
          buildGuideBox("assets/header_icon3.png", "프리미엄 자료로 원하는 사람으로 성장하세요"),
        ],
      ),
    );
  }

  Container buildGuideBox(String iconPath, String text) {
    return Container(
      height: 70,
      margin: EdgeInsets.symmetric(vertical: 10),
      decoration: BoxDecoration(
        color: Color(0xFFDEECE7),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Image.asset(iconPath, width: 40, height: 40),
          Expanded(child: Text(text)),
        ],
      ),
    );
  }

  AppBar buildAppBar() {
    return AppBar(
      title: Row(
        children: [
          Image.asset(
            "assets/logo.png",
            width: 30,
            height: 30,
          ),
          SizedBox(width: 10),
          Text(
            "MBTI 검사 앱",
            style: TextStyle(
              fontSize: 14,
              color: Colors.black,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
      backgroundColor: Colors.white,
    );
  }
}
