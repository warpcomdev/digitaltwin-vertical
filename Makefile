CUE_PKG := "github.com/telefonicasc/digitaltwin-vertical/schema"

all: \
	models/OffStreetParking.json models/TrafficCongestion.json models/TrafficIntensity.json \
	models/RouteSchedule.json models/RouteIntensity.json

models/%.json: schema/models/%.cue schema/types/* schema/templates/* schema/templates/sql/*
	cue export -fo $@ -e '{ "$*": $* }' "${CUE_PKG}/models"

clean:
	rm -f models/*.json && \
	cue fmt schema/types/*.cue && \
	cue fmt schema/templates/*.cue && \
	cue fmt schema/templates/sql/*.cue && \
	cue fmt schema/models/*.cue
