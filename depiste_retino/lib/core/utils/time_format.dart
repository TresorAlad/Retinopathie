/// Formatage personnalisé de l'horodatage de réception d'analyse.
/// Réalisé sans dépendance externe vers le package intl.
abstract final class TimeFormat {
  /// Formate la date de réception selon les règles du cahier des charges :
  /// - Même jour : "Aujourd'hui à HH:mm"
  /// - Autre jour : "jj/MM à HH:mm"
  static String formatReceiptTime(DateTime dateTime) {
    final now = DateTime.now();
    final isSameDay = dateTime.year == now.year &&
        dateTime.month == now.month &&
        dateTime.day == now.day;

    final hours = dateTime.hour.toString().padLeft(2, '0');
    final minutes = dateTime.minute.toString().padLeft(2, '0');

    if (isSameDay) {
      return 'Aujourd\'hui à $hours:$minutes';
    } else {
      final day = dateTime.day.toString().padLeft(2, '0');
      final month = dateTime.month.toString().padLeft(2, '0');
      return '$day/$month à $hours:$minutes';
    }
  }
}
