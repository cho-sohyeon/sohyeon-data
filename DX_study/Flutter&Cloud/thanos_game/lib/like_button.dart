import 'package:flutter/material.dart';

class LikeButton extends StatefulWidget {
  const LikeButton({super.key});

  @override
  State<LikeButton> createState() => _LikeButtonState();
}

class _LikeButtonState extends State<LikeButton> {
  // 좋아요 상태를 나타내는 변수입니다.
  bool _isLiked = false;

  // 화면에 그릴 UI를 정의합니다.
  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(
        Icons.favorite, // 하트 모양 아이콘입니다.
        color: _isLiked ? Colors.red : Colors.grey, // 좋아요 여부에 따라 색상이 바뀝니다.
      ),
      onPressed: () {
        // 좋아요 상태를 바꿔줍니다.
        setState(() {
          _isLiked = !_isLiked;
        });
      },
    );
  }
}
