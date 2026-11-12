/// État de cadrage du visage dans le viseur (analyse locale ML Kit).
enum FramingStatus {
  searching,
  almost,
  ready,
  poorLighting,
}

extension FramingStatusLabel on FramingStatus {
  String get label {
    switch (this) {
      case FramingStatus.searching:
        return 'Cherchez le cadre';
      case FramingStatus.almost:
        return 'Ajustez légèrement';
      case FramingStatus.ready:
        return 'Bien cadré';
      case FramingStatus.poorLighting:
        return 'Éclairez davantage';
    }
  }

  bool get isReady => this == FramingStatus.ready;
}
