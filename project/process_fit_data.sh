for dir in ./fit_data/*/; do
    [ -d "$dir" ] || continue
    for fit in "$dir"/*.fit; do
        [ -f "$fit" ] || continue
        echo "Processing: $fit"
        java -jar FitCSVTool.jar "$fit"
    done
done