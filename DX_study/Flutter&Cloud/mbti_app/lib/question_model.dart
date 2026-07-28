import 'package:mbti_app/answer_model.dart';

// 질문 클래스
class Question {
  final String id;
  final String text; // 질문 내용
  final MBTIType type; // 질문이 속한 MBTI 유형 (E, I, S, N, T, F, J, P)

  Question(this.id, this.text, this.type);
}

// MBTI 유형을 나타내는 Enum
enum MBTIType {
  E, // 외향형(Extraversion)
  I, // 내향형(Introversion)
  S, // 감각형(Sensing)
  N, // 직관형(Intuition)
  T, // 사고형(Thinking)
  F, // 감정형(Feeling)
  J, // 판단형(Judging)
  P, // 인식형(Perceiving)
}

// MBTI 질문 리스트 (총 20개)
List<Question> questions = [
  // 질문 1
  Question("1", "당신은 낯선 도시에서 길을 찾을 때, 지도를 보며 현재 위치를 파악하는 것을 선호합니다.", MBTIType.S),

  // 질문 2
  Question("2", "친구들과의 약속이 갑자기 취소되었을 때, 당신은 그 시간을 활용할 다른 계획을 즉시 세웁니다.", MBTIType.J),

  // 질문 3
  Question("3", "프로젝트를 시작할 때, 완벽한 결과보다 새로운 시도를 해보는 것에 더 흥미를 느낍니다.", MBTIType.P),

  // 질문 4
  Question("4", "복잡한 문제를 해결할 때, 당신은 머릿속에서 다양한 가능성을 시각화합니다.", MBTIType.N),

  // 질문 5
  Question("5", "당신은 토론에서 감정보다 사실과 데이터에 근거하여 의견을 제시합니다.", MBTIType.T),

  // 질문 6
  Question("6", "바쁜 하루를 보낸 후, 당신은 사람들과 어울리며 스트레스를 해소합니다.", MBTIType.E),

  // 질문 7
  Question("7", "당신은 주변 사람들의 기분 변화를 민감하게 느끼고 대응합니다.", MBTIType.F),

  // 질문 8
  Question("8", "새로운 기술을 배울 때, 이론보다는 실습을 통해 배우는 것을 선호합니다.", MBTIType.S),

  // 질문 9
  Question("9", "당신은 일상에서 벗어난 모험이나 여행을 계획하는 것을 즐깁니다.", MBTIType.N),

  // 질문 10
  Question("10", "당신은 의견 충돌이 발생하면 조용히 자신의 입장을 고수합니다.", MBTIType.I),

  // 질문 11
  Question("11", "친구의 어려움을 들었을 때, 공감하며 함께 느끼는 편입니다.", MBTIType.F),

  // 질문 12
  Question("12", "당신은 계획된 일정이 변경되면 불편함을 느낍니다.", MBTIType.J),

  // 질문 13
  Question("13", "문제를 접근할 때, 기존의 방법보다 창의적인 해결책을 찾으려고 합니다.", MBTIType.N),

  // 질문 14
  Question("14", "파티에서 당신은 다양한 사람들과 이야기하며 에너지를 얻습니다.", MBTIType.E),

  // 질문 15
  Question("15", "복잡한 기계를 조립할 때, 설명서 없이도 직관적으로 해결할 수 있습니다.", MBTIType.T),

  // 질문 16
  Question("16", "당신은 종종 자신의 생각에 잠겨 주변의 소음을 인식하지 못합니다.", MBTIType.I),

  // 질문 17
  Question("17", "팀 프로젝트에서 당신은 역할 분담과 일정 관리를 주도합니다.", MBTIType.J),

  // 질문 18
  Question("18", "당신은 새로운 환경에서도 즉흥적으로 적응하고 행동할 수 있습니다.", MBTIType.P),

  // 질문 19
  Question("19", "예술 작품을 감상할 때, 작품이 전달하는 감정과 분위기에 집중합니다.", MBTIType.F),

  // 질문 20
  Question("20", "당신은 목표 달성을 위해 체계적인 계획을 세우기보다 유연하게 접근합니다.", MBTIType.P),
];

// 답변을 점수로 변환하는 함수
int getAnswerValue(AnswerType answer) {
  switch (answer) {
    case AnswerType.strongYes:
      return 3;
    case AnswerType.yes:
      return 2;
    case AnswerType.littleYes:
      return 1;
    case AnswerType.neutral:
      return 0;
    case AnswerType.littleNo:
      return -1;
    case AnswerType.no:
      return -2;
    case AnswerType.strongNo:
      return -3;
  }
}

// 사용자 답변을 기반으로 MBTI 유형을 계산하는 함수
String calculateMBTI(List<Question> questions, List<AnswerType> answers) {
  if (questions.length != answers.length) {
    throw Exception('질문과 답변의 개수가 일치하지 않습니다.');
  }

  int eScore = 0;
  int iScore = 0;
  int sScore = 0;
  int nScore = 0;
  int tScore = 0;
  int fScore = 0;
  int jScore = 0;
  int pScore = 0;

  for (int i = 0; i < questions.length; i++) {
    Question q = questions[i];
    AnswerType a = answers[i];
    int answerValue = getAnswerValue(a);

    switch (q.type) {
      case MBTIType.E:
        eScore += answerValue;
        break;
      case MBTIType.I:
        iScore += answerValue;
        break;
      case MBTIType.S:
        sScore += answerValue;
        break;
      case MBTIType.N:
        nScore += answerValue;
        break;
      case MBTIType.T:
        tScore += answerValue;
        break;
      case MBTIType.F:
        fScore += answerValue;
        break;
      case MBTIType.J:
        jScore += answerValue;
        break;
      case MBTIType.P:
        pScore += answerValue;
        break;
    }
  }

  String type = '';

  // 각 유형별 점수를 비교하여 MBTI 유형 결정
  type += (eScore >= iScore) ? 'E' : 'I';
  type += (sScore >= nScore) ? 'S' : 'N';
  type += (tScore >= fScore) ? 'T' : 'F';
  type += (jScore >= pScore) ? 'J' : 'P';

  return type;
}
