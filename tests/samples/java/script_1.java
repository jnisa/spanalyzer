// Test script 1

import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.OpenTelemetry;

public class Script1 {
    private static final Tracer tracer = OpenTelemetry.getGlobalTracer("script_1_tracer");

    /**
     * Random function that will contain the following opentelemetry resources:
     * - span
     * - span.setAttribute
     */
    public void randomFunction() {
        Span span = tracer.spanBuilder("random_function")
            .startSpan();
        
        try (var scope = span.makeCurrent()) {
            span.setAttribute("attribute_1", "value_1");
            span.setAttribute("attribute_2", "value_2");
        } finally {
            span.end();
        }
    }
}