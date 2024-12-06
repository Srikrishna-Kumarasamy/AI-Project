from clearml.automation.controller import PipelineDecorator

PipelineDecorator.pipeline(
    name="Function-Based Pipeline",
    project="Integrated Project"
)

@PipelineDecorator.component(
    name="summa",  # Step name
    execution_queue="default"  # Optional: Queue for execution
)
def summa():
    for i in range (10):
        print(i)
    return [i for i in range(10)]  

@PipelineDecorator.pipeline(name="Function-Based Pipeline", project = "Integrated Project")
def pipeline_flow():
    # Step 1: Extract data
    extracted_data = summa()
    
    # # Step 2: Transform data
    # transformed_data = data_transformation(data=extracted_data, chunk_size=1)

# Execute the pipeline
if __name__ == "__main__":
    pipeline_flow()

