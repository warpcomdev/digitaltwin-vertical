CUE_PKG := "github.com/telefonicasc/digitaltwin-vertical/schema"

all: \
	models/DayType.json \
	models/Trend.json \
	models/Zone.json \
	models/Simulation.json \
	models/OffStreetParking.json \
	models/TrafficCongestion.json \
	models/TrafficIntensity.json \
	models/RouteSchedule.json \
	models/RouteIntensity.json \
	assets/sql/custom_OffStreetParking.sql \
	assets/sql/custom_RouteIntensity.sql \
	assets/sql/custom_RouteSchedule.sql \
	assets/sql/custom_TrafficCongestion.sql \
	assets/sql/custom_TrafficIntensity.sql

models/%.json: schema/models/%.cue schema/types/* schema/templates/* schema/templates/sql/*
	cue export -fo $@ -e '{ "$*": $* }' "${CUE_PKG}/models"

assets/sql/custom_%.sql: schema/models/%.cue schema/types/* schema/templates/* schema/templates/sql/* export_tool.cue
	cue cmd -t filename=$@ -t model=$* -t section=sql export

clean:
	rm -f models/*.json && \
	rm -f assets/sql/custom_*.sql && \
	cue fmt *_tool.cue && \
	cue fmt schema/types/*.cue && \
	cue fmt schema/templates/*.cue && \
	cue fmt schema/templates/sql/*.cue && \
	cue fmt schema/models/*.cue
