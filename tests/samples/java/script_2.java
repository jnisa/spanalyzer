// Test Script 2

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.common.Attributes;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class Script2 {
    private static final Tracer tracer = OpenTelemetry.getGlobalTracer(Script2.class.getName());
    
    // Create a meter
    private static final Meter meter = OpenTelemetry.getGlobalMeter(Script2.class.getName());
    private static final LongCounter requestCounter = meter.counterBuilder("request_counter")
        .setDescription("Counts the number of requests")
        .build();

    /**
     * Random function that will perform the addition of two values.
     *
     * @param val1 the first value to be added
     * @param val2 the second value to be added
     * @return the sum of the two values
     */
    public int randomFunction1(int val1, int val2) {
        Span span = tracer.spanBuilder("random_function_1").startSpan();
        try (var scope = span.makeCurrent()) {
            span.setAttribute("val1", val1);
            span.setAttribute("val2", val2);
            return val1 + val2;
        } finally {
            span.end();
        }
    }

    /**
     * Random function that will perform the subtraction of two values.
     *
     * @param val1 the first value to be subtracted
     * @param val2 the second value to be subtracted
     * @return the difference of the two values
     */
    public int randomFunction2(int val1, int val2) {
        Span span = tracer.spanBuilder("random_function_2").startSpan();
        
        span.setAttributes(Attributes.builder()
            .put("input_1", val1)
            .put("input_2", val2)
            .build());

        try {
            int result = val1 - val2;
            Map<String, Object> eventAttributes = new HashMap<>();
            eventAttributes.put("operation", "subtraction");
            eventAttributes.put("result", result);
            span.addEvent("calculation_completed", Attributes.builder()
                .put("operation", "subtraction")
                .put("result", String.valueOf(result))
                .build());
            return result;
        } finally {
            span.end();
        }
    }

    /**
     * Random function containing three different spans.
     */
    public void randomFunction3() {
        Span parentSpan = tracer.spanBuilder("random_function_3").startSpan();
        try (var scope = parentSpan.makeCurrent()) {
            Span loadUserSpan = tracer.spanBuilder("load_user_from_db").startSpan();
            try {
                loadUserSpan.addEvent("operation_started", Attributes.builder()
                    .put("timestamp", Instant.now().toString())
                    .put("description", "Load User from DB")
                    .build());
                
                loadUserSpan.addEvent("operation_completed", Attributes.builder()
                    .put("timestamp", Instant.now().toString())
                    .put("description", "User loaded from DB")
                    .build());
            } finally {
                loadUserSpan.end();
            }
        } finally {
            parentSpan.end();
        }
        
        Span lastFunctionSpan = tracer.spanBuilder("last_function").startSpan();
        lastFunctionSpan.end();
    }

    /**
     * Random function demonstrating counter usage.
     */
    public boolean randomFunction4() {
        Span span = tracer.spanBuilder("last_function").startSpan();
        try (var scope = span.makeCurrent()) {
            // Simple counter increment
            requestCounter.add(1);

            // Counter with attributes
            requestCounter.add(1, Attributes.builder()
                .put("endpoint", "/api/v1")
                .put("method", "GET")
                .build());

            // Counter with more attributes
            requestCounter.add(2, Attributes.builder()
                .put("endpoint", "/api/v1")
                .put("method", "POST")
                .put("status", "success")
                .build());

            span.setAttribute("counter_updated", true);
            return true;
        } finally {
            span.end();
        }
    }
}