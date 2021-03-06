# sublime-scss2css

Sublime Text 2 and 3 Plugin to compile scss files to css on save. Requires scss installed on PATH.


# Features

 * Automatically compile scss -> css on save when editing a .scss file in sublime
 * Reports compilation errors
 * Compile all scss files in a directory to css files

NB This plugin requires scss to be in your execution path

# Setting

You can add the scss2css settings like this:

	{
		"autoCompile": true,
		"createCssSourceMaps": false,
		"ignorePrefixedFiles": false,
		"scssBaseDir": "./",
		"scssCommand": false,
		"main_file": false,
		"style" :"compressed", //nested，expanded，compact，compressed
		"minName": false,
		"outputDir": "./",
		"outputFile": "", //[example.css] if left blank uses same name of .scss file
		"showErrorWithWindow": true	
	}

Now the user settings `autoCompile` and `style` will be overriden by the project setting.

# 中文报错

`/Library/Ruby/Gems/2.0.0/gems/sass-3.4.19/lib/sass`

在该路文件里面 `engine.rb`，添加一行代码：
`Encoding.default_external = Encoding.find('utf-8')`
