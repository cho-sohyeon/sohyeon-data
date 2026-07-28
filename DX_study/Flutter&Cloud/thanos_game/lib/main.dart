import 'package:flutter/material.dart';

void main() {
  runApp(ThanosApp());
}

class ThanosApp extends StatefulWidget {
  @override
  State<ThanosApp> createState() => _ThanosAppState();
}

class _ThanosAppState extends State<ThanosApp> {
  List<String> _names = [
    "김동아",
    "김하윤",
    "이준우",
    "김수민",
    "강민정",
    "전경서",
    "곽소윤",
    "이승원",
    "손지헌",
    "조소현",
    "장세미",
    "정수임",
    "조성윤",
    "김민서",
    "노희주",
    "정희원",
    "김민정",
    "이성혁",
    "이정수",
    "장소하",
    "박현지",
    "정희선",
    "김동준",
    "지인환",
  ];

  bool showThanos = false;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text("타노스 게임"),
        ),
        body: buildBody(),
        floatingActionButton: buildFloatingActionButton(),
      ),
    );
  }

  FloatingActionButton buildFloatingActionButton() {
    return FloatingActionButton(
      child: Image.asset(
        "assets/finger_snap.png",
        width: 40,
        height: 40,
      ),
      onPressed: () async {
        // 1명이 남았을 때에는 더이상 실행하지 않음.
        if (_names.length <= 1) {
          return;
        }
        // 타노스 움짤을 보여줌
        setState(() {
          showThanos = true;
        });

        // 3.5초 뒤에 타노스 움짤을 숨김
        await Future.delayed(Duration(milliseconds: 3500));

        setState(() {
          showThanos = false;
        });

        // 참가자의 절반을 날려버림
        setState(() {
          //1. names를 뒤섞는다
          _names.shuffle();

          //2. names의 길이를 잰다. (절반이 얼만큼인지 뒤섞는다)
          int count = (_names.length / 2).toInt();

          //3. names의 절반만 취한다.
          _names = _names.take(count).toList();
        });
      },
    );
  }

  Widget buildBody() {
    return Stack(
      alignment: Alignment.center,
      children: [
        GridView(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            childAspectRatio: 3 / 2,
          ),
          children: [
            for (String name in _names) buildCard(name),
          ],
        ),

        if (showThanos)
          Image.asset(
            "assets/thanos_snap.gif",
          ),
      ],
    );
  }

  Card buildCard(String name) {
    return Card(
      child: Row(
        children: [
          Expanded(
            child: Text(
              name,
              textAlign: TextAlign.center,
            ),
          ),
          IconButton(
            icon: Icon(Icons.delete),
            color: Colors.grey,
            onPressed: () {
              setState(() {
                _names.remove(name);
              });
            },
          ),
        ],
      ),
    );
  }
}
