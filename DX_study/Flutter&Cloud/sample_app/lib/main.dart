import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          title: Text("까페 까페"),
          backgroundColor: Colors.yellow,
        ),
        body: buildBody(),
      ),
    ),
  );
}

Column buildBody() {
  return Column(
    children: [
      // Menu 흰 박스
      buildMenuTitle(),

      // Coffee Hot Ice 까만 박스
      buildBlackBox(),

      // 에스프레소 가격
      buildEspresso(),

      // 두쫀쿠
      buildDuzzoncu(),

      // 아메리카노 가격

      // 까페라떼
    ],
  );
}

Container buildDuzzoncu() {
  return Container(
    width: 100,
    height: 100,
    decoration: BoxDecoration(
      color: Colors.brown,
      borderRadius: BorderRadius.circular(10000),
    ),
    alignment: Alignment.center,
    child: Container(
      width: 70,
      height: 70,
      decoration: BoxDecoration(
        color: Colors.lightGreen,
        borderRadius: BorderRadius.circular(10000),
      ),
    ),
  );
}

Container buildEspresso() {
  return Container(
    height: 80,
    padding: EdgeInsets.all(20),
    child: Row(
      children: [
        Expanded(
          child: Text(
            "에스프레소",
          ),
        ),
        Container(
          width: 100,
          child: Text(
            "3.0",
          ),
        ),
        Container(
          width: 100,
          child: Text(
            "3.5",
          ),
        ),
      ],
    ),
  );
}

Container buildMenuTitle() {
  return Container(
    alignment: Alignment.center,
    child: Text(
      "Menu",
      style: TextStyle(
        fontSize: 36,
        fontWeight: FontWeight.bold,
      ),
    ),
  );
}

Container buildBlackBox() {
  return Container(
    height: 80,
    color: Colors.black,
    padding: EdgeInsets.all(20),
    child: Row(
      children: [
        Expanded(
          child: Text(
            "Coffee",
            style: TextStyle(color: Colors.white),
          ),
        ),
        Container(
          width: 100,
          child: Text(
            "Hot",
            style: TextStyle(color: Colors.white),
          ),
        ),
        Container(
          width: 100,
          child: Text(
            "Ice",
            style: TextStyle(color: Colors.white),
          ),
        ),
      ],
    ),
  );
}
