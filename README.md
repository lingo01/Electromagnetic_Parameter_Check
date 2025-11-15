## 简介 | Introduction

`DeviceChange.py` 是一个用于 CloudPSS 平台 [1] 电磁暂态仿真模型参数自动校验与修正的 Python 脚本。该工具面向机电暂态仿真文件自动转换为 CloudPSS 电磁暂态文件的场景，能够对模型中的各类元件参数进行批量检查、自动修正异常值，并生成详细的日志，提升模型仿真可靠性和自动化程度。

`DeviceChange.py` is a Python script for automatic parameter validation and correction in electromagnetic transient simulation models on the CloudPSS platform [1]. It is designed for scenarios where electromechanical transient simulation files are automatically converted to CloudPSS electromagnetic transient files. The tool batch-checks and auto-corrects abnormal parameters for various components, generating detailed logs to improve model reliability and automation.



[1] Y. Song, Y. Chen, Z. Yu, S. Huang, and C. Shen, ‘CloudPSS: A high-performance power system simulator based on cloud computing’, *Energy Rep.*, vol. 6, pp. 1611–1618, Dec. 2020, doi: [10.1016/j.egyr.2020.12.028](https://doi.org/10.1016/j.egyr.2020.12.028).

<br />

## 免责声明 | Disclaimer

本代码及其相关文档仅供学术研究与技术交流使用。因使用本代码所引发的任何直接或间接损失、故障、法律责任或其他后果，作者概不负责。使用者需自行承担使用本代码的全部风险。

This code and its related documentation are provided solely for academic research and technical exchange. The author assumes no responsibility for any direct or indirect loss, malfunction, legal liability, or other consequences arising from the use of this code. Users bear all risks associated with using this code.

<br />

## 许可协议 | License

本项目采用 [知识共享署名-非商业性使用 4.0 国际许可协议 (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.zh) 发布。

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

<br />

## 联系方式 | Contact

与本代码相关的问题可联系作者彭啸宇（pengxy19@tsinghua.org.cn）进行咨询。

For any questions or uses of the source codes, please feel free to contact the author, Xiaoyu Peng (pengxy19@tsinghua.org.cn), and the corresponding author, Feng Liu (lfeng@mail.tsinghua.edu.cn).

<br />



## 主要功能 | Main Features

- 批量检查和修正发电机、变压器、负荷、直流线路、励磁、调速器等多类元件的参数异常。
- 针对常见的参数越界、缺省、物理不合理等问题，自动赋予合理默认值。
- 适用于 CloudPSS 平台的电磁暂态仿真模型自动化处理流程。

- Batch validation and correction for parameters of generators, transformers, loads, DC lines, exciters, governors, and more.
- Automatically assigns reasonable default values for common issues such as out-of-range, missing, or physically unreasonable parameters.
- Suitable for automated processing of electromagnetic transient simulation models on the CloudPSS platform.


<br />

## 实现思路 | Implementation Approach

1. 通过 CloudPSS Python SDK 访问和操作模型文件。
2. 遍历模型中的各类元件，针对每类元件的典型参数进行物理合理性检查。
3. 对于检测到的异常参数，自动修正为推荐值或安全范围内的默认值。
4. 所有调整均通过日志详细记录，便于后续复查。
5. 支持批量处理和自动保存模型。

1. Access and manipulate model files via the CloudPSS Python SDK.

2. Iterate over various components in the model and perform physical reasonableness checks on key parameters for each type.

3. Automatically correct detected abnormal parameters to recommended or safe default values.

4. All adjustments are logged in detail for later review.

5. Supports batch processing and automatic model saving.

<br />

## 使用方法 | Usage

1. 配置 CloudPSS Python SDK 及相关依赖。
2. 设置 API Token 和模型标识。
3. 运行脚本，自动完成参数校验与修正。
4. 检查生成的日志文件，获取详细调整信息。

1. Configure the CloudPSS Python SDK and related dependencies.
2. Set the API token and model identifier.
3. Run the script to automatically validate and correct parameters.
4. Check the generated log file for detailed adjustment information.

<br />

## 注意事项 | Notes

- 本工具仅用于仿真模型参数自动化校验与修正，不涉及且不用于实际电网数据。
- 请在使用前备份原始模型文件，避免覆盖替换后原始数据丢失。

- This tool is for automated validation and correction of simulation model parameters only, and does not involve any real power grid data.
- Please back up the original model file before use to avoid data loss.



