import 'package:flutter/material.dart';
import 'package:mbti_app/answer_model.dart';
import 'package:mbti_app/question_model.dart';

class QuestionBox extends StatefulWidget {
  const QuestionBox({super.key, required this.question});

  final Question question;

  @override
  State<QuestionBox> createState() => _QuestionBoxState();
}

class _QuestionBoxState extends State<QuestionBox> with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;
0
  AnswerType? selectedAnswer;

  @override
  Widget build(BuildContext context) {
    super.build(context);
    return buildQuestionBox();
  }

  Widget buildCircle(Color color, double size, AnswerType answerType) {
    final isSelected = selectedAnswer == answerType;

    return GestureDetector(
      onTap: () {
        // selectedAnswer를 업데이트 해봅시다!
        setState(() {
          selectedAnswer = answerType;
          allSelectedAnswers[widget.question.id] = answerType;
          print(allSelectedAnswers);
        });
      },
      child: Column(
        children: [
          AnimatedContainer(
            duration: Duration(milliseconds: 600),
            curve: Curves.easeOutBack,
            decoration: BoxDecoration(
              color: isSelected ? color : null,
              border: Border.all(color: color, width: 2),
              borderRadius: BorderRadius.circular(1000),
            ),
            width: selectedAnswer == answerType ? size + 10 : size,
            height: selectedAnswer == answerType ? size + 10 : size,
          ),
        ],
      ),
    );
  }

  Widget buildQuestionBox() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
      ),
      padding: EdgeInsets.all(20),
      child: Column(
        spacing: 10,
        children: [
          // 제목 텍스트
          Text(
            widget.question.text,
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),

          // 동그라미 7개
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              buildCircle(Color(0xFF33A474), 50, AnswerType.strongYes),
              buildCircle(Color(0xFF33A474), 40, AnswerType.yes),
              buildCircle(Color(0xFF33A474), 30, AnswerType.littleYes),
              buildCircle(Colors.grey, 20, AnswerType.neutral),
              buildCircle(Color(0xFF88619A), 30, AnswerType.littleNo),
              buildCircle(Color(0xFF88619A), 40, AnswerType.no),
              buildCircle(Color(0xFF88619A), 50, AnswerType.strongNo),
            ],
          ),

          // 그렇다 / 그렇지않다
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "그렇다",
                style: TextStyle(color: Color(0xFF33A474), fontWeight: FontWeight.bold),
              ),
              Text(
                "그렇지 않다",
                style: TextStyle(color: Color(0xFF88619A), fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
