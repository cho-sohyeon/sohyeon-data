import 'package:flutter/material.dart';
import 'package:portfolio_app/common_app_bar.dart';

class ProjectsPage extends StatelessWidget {
  const ProjectsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: commonAppBar(context, PageType.projects),
      backgroundColor: Color(0xFFF2F2F2),
      body: ListView(
        padding: EdgeInsets.symmetric(horizontal: 100),
        children: [
          Container(height: 60),

          // 1) 페이지 타이틀
          _buildPageTitles(),

          Container(height: 56),

          // 2) 1번째 앱
          _buildProject(
            "assets/project1.jpg",
            "Block Chain App",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
            true,
          ),

          Container(height: 50),

          // 3) 2번째 앱
          _buildProject(
            "assets/project2.jpg",
            "Block Chain App",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
            false,
          ),

          Container(height: 50),

          // 4) 3번째 앱
          _buildProject(
            "assets/project3.jpg",
            "Block Chain App",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
            true,
          ),

          Container(height: 50),

          // 5) 4번째 앱
          _buildProject(
            "assets/project4.jpg",
            "Block Chain App",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
            false,
          ),

          Container(height: 200),
        ],
      ),
    );
  }

  Widget _buildProject(
    String imagePath,
    String title,
    String description,
    bool isLeft,
  ) {
    return Column(
      crossAxisAlignment: isLeft ? CrossAxisAlignment.start : CrossAxisAlignment.end,
      children: [
        // 앱의 이미지
        ClipRRect(
          borderRadius: BorderRadius.circular(20),
          child: Image.asset(
            imagePath,
            width: 600,
            height: 300,
            fit: BoxFit.cover,
          ),
        ),

        Container(height: 18),

        // 앱의 제목
        Text(
          title,
          style: TextStyle(
            fontSize: 24,
            height: 1.0,
            fontWeight: FontWeight.w900,
            color: Color(0xFF38393B),
          ),
        ),

        Container(height: 12),

        // 앱의 설명
        Text(
          description,
          style: TextStyle(
            fontSize: 14,
            height: 18 / 14,
            fontWeight: FontWeight.w300,
            color: Color(0xFF38393B),
          ),
        ),
      ],
    );
  }

  Widget _buildPageTitles() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        RichText(
          text: TextSpan(
            style: TextStyle(
              fontSize: 40,
              height: 1,
              fontWeight: FontWeight.w900,
              fontFamily: "ProductSans",
            ),
            children: [
              TextSpan(
                text: "My ",
                style: TextStyle(color: Color(0xFF38393B)),
              ),
              TextSpan(
                text: "Projects ",
                style: TextStyle(color: Color(0xFF6327E9)),
              ),
              TextSpan(
                text: "Creations",
                style: TextStyle(color: Color(0xFF38393B)),
              ),
            ],
          ),
        ),

        Container(height: 18),

        Container(
          width: 425,
          child: Text(
            "Designing and Developing Robust and Stylish Web Applications for a Decade and Counting",
            style: TextStyle(
              color: Color(0xFF38393B),
              fontSize: 14,
              height: 18 / 14,
              fontWeight: FontWeight.w300,
            ),
          ),
        ),
      ],
    );
  }
}
