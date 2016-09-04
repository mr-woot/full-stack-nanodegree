module.exports = function(grunt) {

    /*Loading our config*/
    var config = grunt.file.readYAML('Gruntconfig.yml');

    /*Load Grunt Tasks*/
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        responsive_images: {
        	dev: {
        		options: {
        			engine: 'im',
        			sizes: [{
        				suffix: '_small',
        				width: 320,
        				quality: 40
        			},
        			{
        				suffix: '_medium',
        				width: 640,
        				quality: 40
        			},
        			{
        				suffix: '_large',
        				width: 800,
        				quality: 40
        			},
        			{
        				suffix: '_x-large',
        				width: 1600,
        				quality: 40
        			}]
        		},
        		files: [{
        			expand: true,
          			src: ['*.{gif,jpg,png,jpeg}'],
        			cwd: 'img_src/',
        			dest: 'img/'
        		}]
        	}
        },
    });
    grunt.registerTask('default', ['responsive_images']);
};
