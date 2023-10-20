/*********************************************************************
 *
 * Licensed Materials - Property of IBM
 *
 * (C) Copyright IBM Corp. 2023. All Rights Reserved.

 * US Government Users Restricted Rights - Use, duplication or
 * disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
 *
 ********************************************************************/

#pragma once

#include <mutex>
#include <string>
#include <vector>
#include <memory>

#include "TreeTypes.hpp"

namespace tree {
class ModelImport;
}

namespace snapml {

class BoosterModel;
class RandomForestModel;
class DenseDataset;

//! @ingroup c-api
class GenericTreeEnsembleModel {
public:
    GenericTreeEnsembleModel();
    void compress(snapml::DenseDataset data);
    void convert_mbit(snapml::DenseDataset data);
    bool check_if_nnpa_installed();
    void get(std::vector<uint8_t>& vec);
    void put(const std::vector<uint8_t>& vec);
    void import_model(const std::string filename, const std::string file_type);
    void export_model(const std::string filename, const std::string file_type, const std::vector<double>& classes,
                      const std::string version);
    bool compressed_tree();
    snapml::task_t     get_task_type();
    uint32_t           get_num_classes();
    std::vector<float> get_class_labels();
    bool               get_class_labels_valid();
    bool               mbit_tree();

    snapml::ensemble_t                         get_ensemble_type() const;
    std::shared_ptr<snapml::BoosterModel>      get_booster_model() const;
    std::shared_ptr<snapml::RandomForestModel> get_rf_model() const;

protected:
    std::shared_ptr<std::mutex>                mtx_;
    std::shared_ptr<tree::ModelImport>         model_parser_;
    std::shared_ptr<snapml::BoosterModel>      booster_model_;
    std::shared_ptr<snapml::RandomForestModel> rf_model_;
};

}