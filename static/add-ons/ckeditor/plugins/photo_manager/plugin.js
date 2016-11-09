CKEDITOR.plugins.add("photo_manager", {
    requires: ["dialog"],
    lang: ["en"],
    init: function (a) {
        var b = "photo_manager";
        var c = a.addCommand(b, new CKEDITOR.dialogCommand(b));
        c.modes = {
            wysiwyg: 1,
            source: 1
        };
        c.canUndo = false;
        a.ui.addButton("Pmanager", {
            label: 'Photo manager',
            command: b,
            icon: this.path + "jezz.png"
        });
        CKEDITOR.dialog.add(b, this.path + "dialogs/photo_manager.js")
    }
});