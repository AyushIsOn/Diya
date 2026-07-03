using DiyaMeditation.Models;

namespace DiyaMeditation.Services;

/// <summary>Swaps the screen shown in the kiosk shell (MainWindow.ContentHost).</summary>
public interface IKioskNavigator
{
    void GoToHome();
    void GoToCalibration(SessionContext context);
    void GoToMeditation(SessionContext context);
    void GoToReport(SessionContext context);
}
