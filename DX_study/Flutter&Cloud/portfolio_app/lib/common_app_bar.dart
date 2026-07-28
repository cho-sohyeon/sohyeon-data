import 'package:flutter/material.dart';

enum PageType {
  home,
  projects,
  contact,
}

PreferredSizeWidget commonAppBar(BuildContext context, PageType selectedPage) {
  // 공통 앱바 위젯을 완성해보세요.
  // selectedPage에 따라 텍스트를 강조해줍니다.
  // 예를 들어 selectedPage가 home이면, home 글씨를 강조해줍니다.
  return AppBar(
    backgroundColor: Color(0xFFF2F2F2),

    title: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, "/");
          },
          child: Text(
            "Home",
            style: TextStyle(
              fontSize: 16,
              color: selectedPage == PageType.home ? Color(0xFF6327E9) : Color(0xFF38393B),
              fontWeight: selectedPage == PageType.home ? FontWeight.w900 : FontWeight.normal, // black weight
            ),
          ),
        ),
        Container(width: 37),
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, "/projects");
          },
          child: Text(
            "Projects",
            style: TextStyle(
              fontSize: 16,
              color: selectedPage == PageType.projects ? Color(0xFF6327E9) : Color(0xFF38393B),
              fontWeight: selectedPage == PageType.projects ? FontWeight.w900 : FontWeight.normal, // black weight
            ),
          ),
        ),
        Container(width: 37),
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, "/contact");
          },
          child: Text(
            "Contact",
            style: TextStyle(
              fontSize: 16,
              color: selectedPage == PageType.contact ? Color(0xFF6327E9) : Color(0xFF38393B),
              fontWeight: selectedPage == PageType.contact ? FontWeight.w900 : FontWeight.normal, // black weight
            ),
          ),
        ),
      ],
    ),
    automaticallyImplyLeading: false,
  );
}
