import 'package:flutter/material.dart';
import 'package:portfolio_app/common_app_bar.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  // 9단계의 폰트 굵기
  // w100: Thin
  // w200: Extra Light
  // w300: Light
  // w400: Regular (Normal)
  // w500: Medium
  // w600: Semi Bold
  // w700: Bold
  // w800: Extra Bold
  // w900: Black

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: commonAppBar(context, PageType.home),
      body: ListView(
        padding: EdgeInsets.symmetric(horizontal: 100),
        children: [
          Container(height: 60),

          // Hero Section
          _buildHero(context),

          // Skills 섹션
          _buildSkills(),

          // Projects 섹션

          // My Story 섹션
        ],
      ),
      backgroundColor: Color(0xFFF2F2F2),
    );
  }

  Container _buildSkills() {
    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(height: 135),

          // 1. 타이틀 (Skills)
          _buildSkillsTitle(),

          Container(height: 30),

          // 2. 본문 내용
          _buildSkillBody(),
          Container(height: 100),
        ],
      ),
    );
  }

  RichText _buildSkillsTitle() {
    return RichText(
      text: TextSpan(
        children: [
          TextSpan(
            text: "Skills",
            style: TextStyle(
              fontSize: 45,
              fontWeight: FontWeight.w900,
              color: Color(0xFF6327E9),
            ),
          ),
          TextSpan(
            text: ".",
            style: TextStyle(
              fontSize: 45,
              fontWeight: FontWeight.w900,
              color: Color(0xFF38393B),
            ),
          ),
        ],
      ),
    );
  }

  Row _buildSkillBody() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // 1. FrontEnd
        _buildSkillColumn(
          "FrontEnd",
          ["JavaScript", "ReactJS", "NextJS"],
        ),

        // 2. BackEnd
        _buildSkillColumn(
          "BackEnd",
          ["JavaScript", "ReactJS"],
        ),

        // 3. App
        _buildSkillColumn(
          "App",
          ["JavaScript", "ReactJS", "NextJS"],
        ),

        // 4. Soft Skills
        _buildSkillColumn(
          "Soft Skills",
          ["JavaScript"],
        ),
      ],
    );
  }

  Widget _buildSkillColumn(String title, List<String> skills) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w900,
            color: Color(0xFF38393B),
          ),
        ),
        Container(height: 10),
        for (var skill in skills)
          Text(
            skill,
            style: TextStyle(
              color: Color(0xFF6A6C70),
              fontSize: 14,
              fontWeight: FontWeight.w300,
            ),
          ),
      ],
    );
  }

  Row _buildHero(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // 1. 프로필 사진
        _buildProfileImage(),

        Container(width: 110),

        // 2. 텍스트 뭉치
        _buildHeroTexts(context),
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
          Text(
            "Hi, I'm sohyeon!",
            style: TextStyle(
              fontSize: 22,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 20),
          Text(
            "Service Product",
            style: TextStyle(
              height: 0.7,
              fontSize: 70,
              fontWeight: FontWeight.w900,
              color: Color(0xFF6327E9),
            ),
          ),
          Text(
            "Manager",
            style: TextStyle(
              fontSize: 70,
              fontWeight: FontWeight.w900,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 20),
          Text(
            "I'm a Service Product Manager based in South Korea.",
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w300,
              color: Color(0xFF38393B),
            ),
          ),
          Container(height: 44),

          // 버튼들
          Row(
            children: [
              // Get In Touch
              _buildGetInTouchButton(context),

              Container(width: 20),

              // Browse Projects
              _buildBrowseProjectsButton(context),
            ],
          ),
        ],
      ),
    );
  }

  GestureDetector _buildGetInTouchButton(BuildContext context) {
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

  GestureDetector _buildBrowseProjectsButton(BuildContext context) {
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
