
from cioblender.buttoned_scroll_panel import ButtonedScrollPanel
from cioblender.notice_grp import NoticeGrp


class ValidationTab(ButtonedScrollPanel):

    def __init__(self, payload, dialog):
        """
       Initialize the ValidationTab.

       Args:
           payload: The payload containing submission data.
           dialog: The parent dialog to which this tab belongs.
       """
        super(ValidationTab, self).__init__(
            dialog,
            buttons=[("close", "Close"), ("continue", "Continue Submission")])
        self.dialog = dialog
        self.payload = payload
        self.configure_signals()

    def configure_signals(self):
        """
        Configure signals for the buttons in the tab.
        """
        self.buttons["close"].clicked.connect(self.dialog.on_close)
        self.buttons["continue"].clicked.connect(self.on_continue)

    def populate(self, errors, warnings, infos):
        """
        Populate the ValidationTab with validation results.

        Args:
            errors (list): A list of error messages.
            warnings (list): A list of warning messages.
            infos (list): A list of informational messages.
        """
        
        obj = {
            "error": errors,
            "warning": warnings,
            "info": infos
        }

        for severity in ["error", "warning", "info"]:
            for entry in obj[severity]:
                has_issues = True
                widget = NoticeGrp(entry, severity)
                self.layout.addWidget(widget)

        has_issues = False
        if not has_issues:
            widget = NoticeGrp("No issues found", "success")
            self.layout.addWidget(widget)

        self.layout.addStretch()

        if errors:
            self.buttons["continue"].setEnabled(False)
        else:
            self.buttons["continue"].setEnabled(True)


    def on_continue(self):
        """
        Handle the "Continue Submission" button click event.

        Trigger the submission process and show the progress tab.
        """
        print("Continue Submission...")

        if self.payload:
            # Show the progress tab
            self.dialog.show_progress_tab()

            print("Submitting jobs...")
            self.dialog.progress_tab.submit(self.payload)



        
 