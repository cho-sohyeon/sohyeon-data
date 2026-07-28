import 'package:flutter/material.dart';
import 'package:portfolio_app/common_app_bar.dart';

class ContactPage extends StatelessWidget {
  const ContactPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF2F2F2),
      appBar: commonAppBar(context, PageType.contact),
      body: ListView(
        padding: EdgeInsets.symmetric(horizontal: 300),
        children: [
          // 1. Hero 뷰
          _buildHero(context),

          Container(height: 25),

          // 2. 연락처
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 이메일 정보
              Row(
                children: [
                  Image.asset(
                    "email_button.png",
                    width: 40,
                    height: 40,
                  ),
                  Container(width: 25),
                  Text(
                    "soheyun0601@gmail.com",
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ],
              ),
              Container(height: 25),

              // 휴대폰 정보
              Row(
                children: [
                  Image.asset(
                    "phone_button.png",
                    width: 40,
                    height: 40,
                  ),
                  Container(width: 25),
                  Text(
                    "+82-10-8572-2285",
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ],
              ),
              Container(height: 100),
            ],
          ),
        ],
      ),
    );
  }

  Row _buildHero(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        // 2. 텍스트 뭉치
        _buildHeroTexts(context),

        Container(width: 110),

        // 1. 프로필 사진
        _buildProfileImage(),
      ],
    );
  }

  Container _buildProfileImage() {
    return Container(
      width: 286,
      height: 286,
      decoration: BoxDecoration(
        border: Border.all(
          color: Color(0xFF6327E9),
          width: 1,
        ),
        borderRadius: BorderRadius.circular(1000),
      ),
      padding: EdgeInsets.all(30),
      child: Container(
        width: 230,
        height: 230,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(1000),
          child: Image.asset(
            "assets/엄.jpg",
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }

  Widget _buildHeroTexts(BuildContext context) {
    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(height: 100),
          Text(
            "Hi, I'm sohyeon!",
            style: TextStyle(
              fontSize: 22,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 20),
          Text(
            "Get in",
            style: TextStyle(
              height: 0.7,
              fontSize: 70,
              fontWeight: FontWeight.w900,
              color: Color(0xFF6327E9),
            ),
          ),
          Text(
            "Touch",
            style: TextStyle(
              fontSize: 70,
              fontWeight: FontWeight.w900,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 20),
          Text(
            "Looking to partner or work together.",
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w300,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 44),
        ],
      ),
    );
  }

  GestureDetector buildGetInTouchButton(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.pushNamed(context, "/contact");
      },
      child: Container(
        width: 153,
        height: 56,
        decoration: BoxDecoration(
          color: Color(0xFF6327E9),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Center(
          child: Text(
            "Get In Touch",
            style: TextStyle(
              fontSize: 16,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }

  GestureDetector buildBrowseProjectsButton(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.pushNamed(context, "/projects");
      },
      child: Container(
        width: 153,
        height: 56,
        decoration: BoxDecoration(
          border: Border.all(),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Center(
          child: Text(
            "Browse Projects",
            style: TextStyle(
              fontSize: 16,
              color: Color(0xFF38393B),
            ),
          ),
        ),
      ),
    );
  }
}
