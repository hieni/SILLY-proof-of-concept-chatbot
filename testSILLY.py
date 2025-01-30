# testSILLY.py - A simple testing script to demonstrate automatic unit testing - Proof of Concept
import os
from SILLY import save_topics, load_topics, TOPICS_CACHE_FILE

# Setup function for assumed test data
def setUp():
    topics = {
        "agent": {"human", "agent", "employee"},
        "email": {"email", "mail"},
    }
    cache_file = TOPICS_CACHE_FILE
    return topics, cache_file

# Cleanup function
def cleanUp(cache_file):
    if os.path.exists(cache_file):
        os.remove(cache_file)

# Test if save_topics correctly saves data to file
def test_save_topics():
    topics, cache_file = setUp()
    
    # Convert sets to lists for json
    topics_json_compatible = {key: list(value) for key, value in topics.items()}
    
    # Save topics and check cache file creation
    save_topics(topics_json_compatible)
    assert os.path.exists(cache_file), "Cache file should be created."
    
    cleanUp(cache_file)

# Test if load_topics correctly loads data
def test_load_topics():
    topics, cache_file = setUp()
    
    # Save topics first (convert to list for json)
    topics_json_compatible = {key: list(value) for key, value in topics.items()}
    save_topics(topics_json_compatible)
    
    # Test load_topics to make sure it loads the data correctly
    loaded_data = load_topics()
    
    # Convert loaded data back to sets for comparison
    loaded_data_sets = {key: set(value) for key, value in loaded_data.items()}
    assert loaded_data_sets == topics, "Loaded topics should match saved data."
    
    # Test loading from a non-existing file
    if os.path.exists(cache_file):
        os.remove(cache_file)  # Simulate missing cache
    loaded_data = load_topics()
    assert loaded_data is None, "Loading from a non-existent file should return None."
    
    cleanUp(cache_file)



# Test for handling of a bogus cache file
def test_bogus_cache():
    topics, cache_file = setUp()
    
    # Create a bogus cache file (invalid JSON)
    with open(cache_file, 'w') as f:
        f.write("{ this is not: 'valid JSON' ")  # Malformed JSON
    
    # Test load_topics to ensure it handles the invalid cache gracefully
    loaded_data = load_topics()
    
    # Assert that load_topics returns None when it fails to decode the cache
    assert loaded_data is None, "Loading a bogus cache should return None."
    
    cleanUp(cache_file)

# Running the tests
if __name__ == "__main__":
    test_save_topics()
    print("###Test save topics passed.###")
    test_load_topics()
    print("###Test load topics passed.###")
    test_bogus_cache()
    print("###Test bogus cache passed.###")
    print("######All tests passed.######")
