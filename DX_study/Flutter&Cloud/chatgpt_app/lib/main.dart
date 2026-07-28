import 'package:chatgpt_app/model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gemini/flutter_gemini.dart';

void main() {
  runApp(ChatGptApp());
}

class ChatGptApp extends StatefulWidget {
  ChatGptApp({super.key});

  @override
  State<ChatGptApp> createState() => _ChatGptAppState();
}

class _ChatGptAppState extends State<ChatGptApp> {
  ChatRoom room = ChatRoom(chats: [], createdAt: DateTime.now());

  final TextEditingController controller = TextEditingController();
  final FocusNode focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    Gemini.init(apiKey: "AQ.Ab8RN6KEAn7pL4OC4Ag_LHcmmuoDPvFL_d0O7UN07mADLsZN2g");
  }

  @override
  void dispose() {
    controller.dispose();
    focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: buildAppBar(),
        backgroundColor: Colors.white,
        body: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            // 빈페이지를 구현해보세요 (Image 위젯을 사용해서 로고 이미지를 한 가운데에 보여줍니다.)
            if (room.chats.isEmpty) buildEmpty(),
            if (room.chats.isNotEmpty) buildChatBody(),
            buildTextField(),
          ],
        ),
      ),
    );
  }

  Widget buildChatBody() {
    if (room.chats.isEmpty) {
      return Container();
    }
    return Expanded(
      child: ListView(
        children: [
          for (ChatMessage message in room.chats)
            message.isMe ? buildMyChatBubble(message) : buildGptChatBubble(message),
        ],
      ),
    );
  }

  Widget buildMyChatBubble(ChatMessage message) {
    return Align(
      alignment: Alignment.centerRight,
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        constraints: BoxConstraints(
          maxWidth: 200,
        ),
        decoration: BoxDecoration(
          color: const Color.fromARGB(65, 255, 239, 58),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(message.text),
      ),
    );
  }

  Widget buildGptChatBubble(ChatMessage message) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        child: Row(
          spacing: 10,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image.asset(
              "assets/logo.png",
              width: 30,
              height: 30,
            ),
            Container(
              padding: EdgeInsets.all(4),
              constraints: BoxConstraints(
                maxWidth: 200,
              ),
              decoration: BoxDecoration(
                color: const Color.fromARGB(4, 255, 239, 58),
                border: Border.all(
                  color: Colors.grey[300]!,
                  width: 1,
                ),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(message.text),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildEmpty() {
    return Expanded(
      child: Center(
        child: Image.asset(
          "assets/rabbit.gif",
          width: 200,
          height: 200,
        ),
      ),
    );
  }

  Container buildTextField() {
    return Container(
      margin: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color.fromARGB(65, 255, 239, 58),
        borderRadius: BorderRadius.circular(1000),
      ),
      child: TextField(
        controller: controller,
        focusNode: focusNode,
        onSubmitted: sendMessage,
        onChanged: (value) {
          //현재 입력된 글씨가 있으면 sendButtonEnabled를 true로 바꾼다. 아니면 false로 바꾼다.
          setState(() {
            sendButtonEnabled = value.isNotEmpty;
          });
        },
        // TextField 꾸미기
        decoration: InputDecoration(
          hintText: '메시지',
          border: InputBorder.none,
          contentPadding: EdgeInsets.symmetric(horizontal: 15.0, vertical: 20.0),
          suffixIcon: buildSendButton(),
        ),
        // TextField 글꼴 바꾸기
        style: TextStyle(
          fontSize: 14,
        ),
      ),
    );
  }

  void sendMessage(String text) {
    // 0. room.chats에 방금 보낸 메시지를 추가한다.
    final ChatMessage newMessage = ChatMessage(
      isMe: true,
      text: text,
      sentAt: DateTime.now(),
    );
    setState(() {
      room.chats.add(newMessage);
    });

    // 1. 모든 글씨를 지운다.
    controller.clear();
    // 2. 포커스를 회수한다.
    focusNode.unfocus();
    // 3. 전송버튼을 비활성화 한다.
    setState(() {
      sendButtonEnabled = false;
    });

    generateResponse(text);
  }

  void generateResponse(String question) {
    // Gemini가 보낸 메시지를 담을 수 있는 말풍선을 미리 추가한다!
    final ChatMessage gptMessage = ChatMessage(
      isMe: false,
      text: "응답 중...",
      sentAt: DateTime.now(),
    );

    setState(() {
      room.chats.add(gptMessage);
    });

    // 실제로 Gemini 한테 응답을 요청하고 받는 코드
    Gemini.instance
        .promptStream(
          parts: [Part.text(question)],
          model: "gemini-2.5-flash",
        )
        .listen((event) {
          final String answer = (event?.output ?? "응답이 없습니다");
          setState(() {
            room.chats.last.text += answer;
          });
        });
  }

  bool sendButtonEnabled = false;

  Container buildSendButton() {
    return Container(
      margin: EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: sendButtonEnabled ? const Color.fromARGB(255, 255, 239, 58) : const Color.fromARGB(24, 255, 239, 58),
        borderRadius: BorderRadius.circular(1000),
      ),
      child: IconButton(
        icon: Icon(
          Icons.arrow_upward_rounded,
          color: Colors.white,
        ),
        onPressed: () {
          sendMessage(controller.text);
        },
      ),
    );
  }

  AppBar buildAppBar() {
    return AppBar(
      title: Text(
        "🤍 소현콩의 ChatGPT 🤍",
        style: TextStyle(
          fontSize: 14,
          color: Colors.black,
          fontWeight: FontWeight.bold,
        ),
      ),
      centerTitle: true,
      backgroundColor: const Color.fromARGB(148, 255, 239, 58),
      surfaceTintColor: Colors.transparent,
      elevation: 12,
      shadowColor: Colors.grey[50],
    );
  }
}
