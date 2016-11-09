CKEDITOR.plugins.add("music_manager", {
    requires: ["dialog"],
    lang: ["en"],
    init: function (a) {
        var b = "music_manager";
        var c = a.addCommand(b, new CKEDITOR.dialogCommand(b));
        c.modes = {
            wysiwyg: 1,
            source: 1
        };
        c.canUndo = false;
        a.ui.addButton("Mmanager", {
            label: 'Music manager',
            command: b,
            icon: this.path + "jezz.png"
        });
        CKEDITOR.dialog.add(b, this.path + "dialogs/music_manager.js")
    }
});