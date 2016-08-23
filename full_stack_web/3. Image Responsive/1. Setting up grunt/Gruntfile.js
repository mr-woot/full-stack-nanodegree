module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-sass');

    grunt.initConfig({
        sass: {
            dist: {
                src: 'sass/style.scss',
                dest: 'css/style2.css'
            }
        }
    });

    grunt.registerTask('default', [
        'sass'
    ]);
};
