package cmd

import (
	"text/template"
	"strings"
	"tool/file"
	"github.com/telefonicasc/digitaltwin-vertical/schema/models"
)

#filename: string @tag(filename)
#model:    string @tag(model)

command: sql: render: file.Create & {
	filename: #filename
	contents: strings.Join([for label, tmpl in models[#model].#sql_template {
		template.Execute(tmpl.sql, tmpl.input)
	}], "\n\n")
}
