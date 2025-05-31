// Test script 4

import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.context.Scope;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import java.util.HashMap;

public class Script4 {
    private static final Tracer tracer = OpenTelemetry.getGlobalTracer("script_4_tracer");

    /**
     * Simulate async data fetch with delay.
     */
    private CompletableFuture<Map<String, List<Integer>>> fetchMockData() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(100); // Simulate network delay
                Map<String, List<Integer>> result = new HashMap<>();
                result.put("data", List.of(1, 2, 3, 4, 5));
                return result;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        });
    }

    /**
     * Simulate async data processing.
     */
    private CompletableFuture<List<Integer>> processMockData(Map<String, List<Integer>> data) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(50); // Simulate processing time
                return data.get("data").stream()
                    .map(x -> x * 2)
                    .collect(Collectors.toList());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        });
    }

    /**
     * Async function that fetches data with telemetry.
     */
    public CompletableFuture<List<Integer>> asyncFetchData() {
        Span span = tracer.spanBuilder("fetch_data").startSpan();
        
        return CompletableFuture.supplyAsync(() -> {
            try (Scope scope = span.makeCurrent()) {
                span.setAttribute("request_type", "async");
                
                return fetchMockData()
                    .thenCompose(rawData -> {
                        span.setAttribute("data_size", rawData.get("data").size());
                        
                        return processMockData(rawData)
                            .thenApply(processedData -> {
                                span.addEvent("data_processed", Attributes.builder()
                                    .put("input_size", rawData.get("data").size())
                                    .put("output_size", processedData.size())
                                    .build());
                                return processedData;
                            });
                    })
                    .exceptionally(throwable -> {
                        span.recordException(throwable);
                        throw new CompletionException(throwable);
                    })
                    .join();
            } finally {
                span.end();
            }
        });
    }

    // Example usage
    public static void main(String[] args) {
        Script4 script = new Script4();
        script.asyncFetchData()
            .thenAccept(result -> System.out.println("Processed data: " + result))
            .exceptionally(throwable -> {
                System.err.println("Error: " + throwable.getMessage());
                return null;
            });
    }
}