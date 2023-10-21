#ifdef IMGUI_BUNDLE_WITH_TEST_ENGINE
#define IMGUI_DEFINE_MATH_OPERATORS
#include "imgui.h"
#include "hello_imgui/hello_imgui.h"
#include "imgui_test_engine/imgui_te_ui.h"
#include "imgui_test_engine/imgui_te_engine.h"
#include "imgui_test_engine/imgui_te_context.h"


ImGuiTest *test_open_metric, *test_capture_screenshot;


#include <mutex>
#include <fplus/fplus.hpp>
struct AutomationInfoBubble
{
    void SetMessage(const std::string& info)
    {
        std::lock_guard guard(MessageMutex);
        CurrentMessage = info;
    }

    void Gui()
    {
        _UpdateInternals();

        std::string currentMessageCopy;
        {
            std::lock_guard guard(MessageMutex);
            currentMessageCopy = CurrentMessage;
        }

        if (currentMessageCopy.empty())
            return;

        ImVec2 infoWindowSize = HelloImGui::EmToVec2(40, 4);
        ImVec2 infoWindowPosition =
            ImGui::GetMainViewport()->Pos + ImGui::GetMainViewport()->Size - infoWindowSize;

        ImGui::SetNextWindowPos(infoWindowPosition);
        ImGui::SetNextWindowSize(infoWindowSize);
        ImGui::Begin("Bubble");
        ImGui::TextWrapped("%s", currentMessageCopy.c_str());
        ImGui::End();
    }

    void SetDurationSeconds(float durationSeconds)
    {
        std::lock_guard guard(MessageMutex);
        Duration = durationSeconds;
    }

private:
    void _UpdateInternals()
    {
        double now = Watch.elapsed();

        // if new message, reset clock
        if (CurrentMessage != LastDisplayedMessage)
        {
            LastDisplayStartTime = Watch.elapsed();
            LastDisplayedMessage = CurrentMessage;
        }

        // Hide message if duration elapsed
        if (! CurrentMessage.empty())
        {
            if ( (now - LastDisplayStartTime) > Duration)
            {
                CurrentMessage = "";
                LastDisplayedMessage = "";
                LastDisplayStartTime = 0.;
            }
        }
    }

private:
    fplus::stopwatch Watch;
    std::mutex MessageMutex;
    std::string CurrentMessage;
    std::string LastDisplayedMessage;
    double LastDisplayStartTime = 0.0;
    double Duration = 3.0;
};

AutomationInfoBubble GAutomationInfoBubble;


void MyRegisterTests()
{
    auto engine = HelloImGui::GetImGuiTestEngine();

    //-----------------------------------------------------------------
    // ## Open Metrics window
    //-----------------------------------------------------------------

    test_open_metric = IM_REGISTER_TEST(engine, "demo_tests", "open_metrics");
    test_open_metric->TestFunc = [](ImGuiTestContext* ctx)
    {
        ctx->SetRef("Dear ImGui Demo");
        ctx->MenuCheck("Tools/Metrics\\/Debugger");
    };

    //-----------------------------------------------------------------
    // ## Capture entire Dear ImGui Demo window.
    //-----------------------------------------------------------------

    test_capture_screenshot = IM_REGISTER_TEST(engine, "demo_tests", "capture_screenshot");
    test_capture_screenshot->TestFunc = [](ImGuiTestContext* ctx)
    {
        GAutomationInfoBubble.SetMessage("Clicking on the window Dear ImGui Demo");
        //ctx->WindowBringToFront("Dear ImGui Demo");
        ctx->ItemClick("Dear ImGui Demo");
        ctx->SleepStandard();
        ctx->Sleep(3.f);

        GAutomationInfoBubble.SetMessage("Opening Widgets/Basic");
        ctx->SetRef("Dear ImGui Demo");
        ctx->ItemOpen("Widgets");       // Open collapsing header
        ctx->ItemOpenAll("Basic");      // Open tree node and all its descendant
        ctx->SleepStandard();

        GAutomationInfoBubble.SetMessage("Capturing screenshot");
        ctx->CaptureScreenshotWindow("Dear ImGui Demo", ImGuiCaptureFlags_StitchAll | ImGuiCaptureFlags_HideMouseCursor);
        ctx->SleepStandard();
    };

}

void AppGui()
{
    auto engine = HelloImGui::GetImGuiTestEngine();
    ImGui::ShowDemoWindow();
    ImGuiTestEngine_ShowTestEngineWindows(engine, NULL);
    GAutomationInfoBubble.Gui();

    if (ImGui::Button("Run open metric automation"))
        ImGuiTestEngine_QueueTest(engine, test_open_metric);
    if (ImGui::Button("Run capture screenshot automation"))
        ImGuiTestEngine_QueueTest(engine, test_capture_screenshot);
}


int main(int, char**)
{
    HelloImGui::RunnerParams runnerParams;
    runnerParams.useImGuiTestEngine = true;

    runnerParams.callbacks.ShowGui = AppGui;
    runnerParams.callbacks.RegisterTests = MyRegisterTests;
    HelloImGui::Run(runnerParams);
}

#else // #ifdef IMGUI_BUNDLE_WITH_TEST_ENGINE
int main(int, char**) {}
#endif